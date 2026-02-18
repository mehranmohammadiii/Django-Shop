from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from accounts.models import UserType
from ..permissions import HasCustomerAccesPermission
from django.contrib.auth import views as auth_view
from .forms import CustomerPasswordChangeForm,CustomerProfileEditForm,CustomerAddressForm
from accounts.models import Profile
from order.models import UserAddress, Order
from shop.models import wishlist
# -----------------------------------------------------------------------------------------
class CustomerDashboardHomeView(LoginRequiredMixin,HasCustomerAccesPermission, TemplateView):
    template_name = 'dashboard/customer/home.html'
    
    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         if request.user.type != UserType.ADMIN.value:
    #             return redirect(reverse_lazy('dashboard:home'))
    #     return super().dispatch(request, *args, **kwargs)

# -----------------------------------------------------------------------------------------
class CustomerSecurityEditView(LoginRequiredMixin, HasCustomerAccesPermission, auth_view.PasswordChangeView):   
    template_name = 'dashboard/customer/security_edit.html'
    success_url = reverse_lazy('dashboard:customer:security-edit')
    form_class = CustomerPasswordChangeForm
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'رمز عبور شما با موفقیت تغییر یافت.')
        return response
    # -----------------------------------    
    def form_invalid(self, form):
        # نمایش خطاهای form از طریق messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return self.render_to_response(self.get_context_data(form=form))
# -----------------------------------------------------------------------------------------
class CustomerProfileEditView(LoginRequiredMixin, HasCustomerAccesPermission, UpdateView):
    template_name = 'dashboard/customer/profile_edit.html'
    success_url = reverse_lazy('dashboard:customer:profile-edit')
    form_class = CustomerProfileEditForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'پروفایل شما با موفقیت به‌روزرسانی شد.')
        return response
    
    def get_object(self, queryset=None):
        # اگر Profile وجود نداشت، یک جدید ایجاد کن
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
# -------------------------------------------------------------------------------------------  
class CustomerProfileImageEditView(LoginRequiredMixin, HasCustomerAccesPermission, UpdateView):
    http_method_names = ["post"]
    success_url = reverse_lazy('dashboard:customer:profile-edit')
    model = Profile
    fields = ['image']

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'تصویر پروفایل شما با موفقیت به‌روزرسانی شد.')
        return response
    
    def get_object(self, queryset=None):
        # اگر Profile وجود نداشت، یک جدید ایجاد کن
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    def form_invalid(self, form):
        # نمایش خطاهای form از طریق messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect(self.success_url)
# -------------------------------------------------------------------------------------------  
class CustomerAddressListView(LoginRequiredMixin, HasCustomerAccesPermission, TemplateView):
    template_name = 'dashboard/customer/address/address_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = UserAddress.objects.filter(user=self.request.user)
        return context
# -------------------------------------------------------------------------------------------  
class CustomerAddressCreateView(LoginRequiredMixin, HasCustomerAccesPermission, CreateView):
    template_name = 'dashboard/customer/address/address_create.html'
    model = UserAddress
    form_class = CustomerAddressForm
    success_url = reverse_lazy('dashboard:customer:address-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'آدرس جدید با موفقیت اضافه شد.')
        return response

# -------------------------------------------------------------------------------------------  
class CustomerAddressEditView(LoginRequiredMixin, HasCustomerAccesPermission, UpdateView):
    template_name = 'dashboard/customer/address/address_edit.html'
    model = UserAddress
    form_class = CustomerAddressForm
    success_url = reverse_lazy('dashboard:customer:address-list')

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'آدرس با موفقیت ویرایش شد.')
        return response
# -------------------------------------------------------------------------------------------  
class CustomerAddressDeleteView(LoginRequiredMixin, HasCustomerAccesPermission, DeleteView):
    template_name = 'dashboard/customer/address/address_delete.html'
    model = UserAddress
    success_url = reverse_lazy('dashboard:customer:address-list')

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        # Get object before deletion
        self.object = self.get_object()
        object_name = self.object.city
        
        # Delete it
        response = super().post(request, *args, **kwargs)
        
        # Add success message AFTER deletion but before redirect
        messages.success(request, f'آدرس "{object_name}" با موفقیت حذف شد.')
        
        return response
# -------------------------------------------------------------------------------------------  
class CustomerOrderListView(LoginRequiredMixin, HasCustomerAccesPermission, TemplateView):

    template_name = 'dashboard/customer/orders/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get search query
        search_query = self.request.GET.get('q', '').strip()
        context['search_query'] = search_query

        all_orders = Order.objects.filter(user=self.request.user).prefetch_related('items__product')
        
        if search_query:
            all_orders = all_orders.filter(
                Q(id__icontains=search_query) |
                Q(items__product__name__icontains=search_query) |
                Q(items__product__category__name__icontains=search_query)
            ).distinct()
        
        # فیلتر کردن سفارشات بر اساس وضعیت
        pending = all_orders.filter(status=1)
        processing_shipped = all_orders.filter(status__in=[2, 3])
        delivered = all_orders.filter(status=4)
        canceled = all_orders.filter(status=5)
        
        # صفحه بندی
        paginator1 = Paginator(pending, 2)
        page1 = self.request.GET.get('page1', 1)
        context['pending_orders'] = paginator1.get_page(page1)
        context['paginator1'] = paginator1
        
        paginator2 = Paginator(processing_shipped, 2)
        page2 = self.request.GET.get('page2', 1)
        context['processing_shipped_orders'] = paginator2.get_page(page2)
        context['paginator2'] = paginator2
        
        paginator3 = Paginator(delivered, 2)
        page3 = self.request.GET.get('page3', 1)
        context['delivered_orders'] = paginator3.get_page(page3)
        context['paginator3'] = paginator3
        
        paginator4 = Paginator(canceled, 2)
        page4 = self.request.GET.get('page4', 1)
        context['canceled_orders'] = paginator4.get_page(page4)
        context['paginator4'] = paginator4
        
        # تعداد کل برای هر گروه
        context['pending_count'] = pending.count()
        context['active_count'] = processing_shipped.count()
        context['delivered_count'] = delivered.count()
        context['canceled_count'] = canceled.count()
        
        return context
# -----------------------------------------------------------------------------------------
class CustomerOrderDetailView(LoginRequiredMixin, HasCustomerAccesPermission, DetailView):
    template_name = 'dashboard/customer/orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset
# -----------------------------------------------------------------------------------------
class CustomerWishlistView(LoginRequiredMixin, HasCustomerAccesPermission, TemplateView):
    template_name = 'dashboard/customer/wishlist/wishlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wishlist_items = wishlist.objects.filter(user=self.request.user).select_related('product')
        context['wishlist_items'] = wishlist_items
        return context    
# -----------------------------------------------------------------------------------------
class CustomerWishlistRemoveView(LoginRequiredMixin, HasCustomerAccesPermission, DeleteView):
    model = wishlist
    success_url = reverse_lazy('dashboard:customer:wishlist')

    def get_queryset(self):
        return wishlist.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        product_name = self.object.product.name
        response = super().post(request, *args, **kwargs)
        messages.success(request, f'محصول "{product_name}" با موفقیت از لیست علاقه‌مندی‌ها حذف شد.')
        return response
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
