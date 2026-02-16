from django.contrib.auth.mixins import LoginRequiredMixin
from .permissions import HasCustomerAccesPermission
from django.views.generic import TemplateView , FormView
from .models import UserAddress, Coupon
from shop.models import Product
from cart.cart import CartSession
from decimal import Decimal
from cart.models import Cart
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .models import Order, OrderItem, UserAddress
from .form import CheckOutForm
from django.http import JsonResponse
from django.views import View
import json
from django.views import View
from django.http import JsonResponse
from django.utils import timezone
from payment.zarinpal_client import ZarinPalSandbox
from payment.models import Payment
# -----------------------------------------------------------------------------------------------------------------------
class CheckoutView(LoginRequiredMixin, HasCustomerAccesPermission, FormView):
    template_name = 'order/checkout.html'
    form_class = CheckOutForm
    success_url = reverse_lazy('order:checkout-complete')
    # -------------------------------------
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    # -------------------------------------
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # فراخوانی آدرس‌های کاربر
        user_addresses = UserAddress.objects.filter(user=user)
        context['user_addresses'] = user_addresses
        
        # فراخوانی سبد خرید
        cart = Cart.objects.filter(user=user).first()
        
        if cart:
            total_price = cart.calculate_total_price()
        else:
            total_price = 0
            
        context['total_price'] = total_price

        # محاسبه مالیات
        tax = total_price * Decimal('9') / Decimal('100')
        context['tax'] = tax

        # محاسبه هزینه ارسال (فعلاً ثابت)
        # تهران و حومه
        shipping_cost = Decimal('35000')  

        # کل نهایی
        final_total = total_price + shipping_cost + tax

        context['shipping_cost'] = shipping_cost
        context['final_total'] = final_total

        return context
    # -------------------------------------       
    def form_valid(self, form):
        # دریافت coupon اگر موجود باشد
        coupon = getattr(form, 'coupon', None)

        address = UserAddress.objects.get(user=self.request.user)
        cart = Cart.objects.filter(user=self.request.user).first()
        cart_items = cart.items.all()      
  
        order = Order.objects.create(
            address=address,
            user=self.request.user,
            )
        
        for item in cart_items :
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            
        cart.items.all().delete()
        CartSession(self.request.session).clear()

        total_price = order.calculate_total_price()
        if coupon:
            total_price = total_price * (Decimal('100') - coupon.discount_percentage) / Decimal('100')
            order.coupon = coupon
            # اضافه کردن کاربر به used_by
            coupon.used_by.add(self.request.user)

        tax = total_price * Decimal('9') / Decimal('100')
        shipping_cost = Decimal('35000')  
        order.total_price = total_price + shipping_cost + tax
        order.save()

        payment_response = self.create_payment(order)
        if payment_response:
            return payment_response
        
        messages.success(self.request, "سفارش شما با موفقیت ثبت شد.")
        return super().form_valid(form)
    # -------------------------------------
    def create_payment(self,order):

        zarin_pal_sandbox = ZarinPalSandbox() 
        response = zarin_pal_sandbox.payment_request(amount=int(order.total_price), description=f"پرداخت سفارش #{order.id}")
        
        # بررسی خطا
        if response.get('errors'):
            messages.error(self.request, f"خطا در درخواست پرداخت: {response['errors']}")
            return redirect('order:checkout')
        
        if response.get('data') and response['data'].get('authority'):
            authority_code = response['data'].get('authority')
            payment_page_url = zarin_pal_sandbox.get_payment_page_url(authority_code)
            print('   authority_code   ')
            print(authority_code)
            payment_obj= Payment.objects.create(
                authority_code=authority_code,
                amount=order.total_price,
            )   
            order.peyment = payment_obj
            order.save()
            return redirect(payment_page_url)
        else:
            messages.error(self.request, "خطا در درخواست پرداخت. لطفاً دوباره تلاش کنید.")
            return redirect('order:checkout')
# ------------------------------------------------------------------------------------------------------------------------------------
class CompletedView(LoginRequiredMixin, HasCustomerAccesPermission, TemplateView):
    template_name = 'order/checkout_complete.html'
# ----------------------------------------------------------------------------------------------------------------------------------
class FailedView(LoginRequiredMixin, HasCustomerAccesPermission, TemplateView):
    template_name = 'order/checkout_failed.html'
# ----------------------------------------------------------------------------------------------------------------------------------
class validate_coupon(LoginRequiredMixin, HasCustomerAccesPermission, View):

    def post(self, request, *args, **kwargs):

        tota_price = 0
        tax = 0
        shipping_cost = 0

        try:
            data = json.loads(request.body)
            coupon_code = data.get('coupon_code', '').strip()
        except json.JSONDecodeError:
            coupon_code = request.POST.get('coupon_code', '').strip()
        
        user = request.user
        valid = True
        message = "کد تخفیف با موفقیت تأیید شد."

        if not coupon_code:
            return JsonResponse({'valid': False, 'message': 'لطفاً کد تخفیف را وارد کنید.'})

        try:
            coupon_obj = Coupon.objects.get(code=coupon_code, active=True)
        except Coupon.DoesNotExist:
            return JsonResponse({'valid': False, 'message': 'کد تخفیف وارد شده معتبر نیست.'})
        
        # بررسی حد استفاده
        if coupon_obj.used_by.count() >= coupon_obj.max_limit_usage:
            return JsonResponse({'valid': False, 'message': 'این کد تخفیف به حد نصاب استفاده رسیده است.'})
        
        # بررسی تاریخ انقضا
        elif coupon_obj.expiration_date and coupon_obj.expiration_date < timezone.now():
            return JsonResponse({'valid': False, 'message': 'این کد تخفیف منقضی شده است.'})
        
        # بررسی استفاده قبلی
        elif user in coupon_obj.used_by.all():
            return JsonResponse({'valid': False, 'message': 'شما قبلاً از این کد تخفیف استفاده کرده‌اید.'})

        else:
            cart = Cart.objects.filter(user=user).first()
            if cart:
                total_price = cart.calculate_total_price()
            else:
                total_price = 0
            total_price = total_price * (Decimal('100') - coupon_obj.discount_percentage) / Decimal('100')
            tax = total_price * Decimal('9') / Decimal('100')
            shipping_cost = Decimal('35000')
            final_total = total_price + shipping_cost + tax

        return JsonResponse({'valid': True, 'tax' : tax,'final_total': final_total, 'message': 'کد تخفیف معتبر است!', 'discount': coupon_obj.discount_percentage})
# -----------------------------------------------------------------------------------------------------------------------------------
