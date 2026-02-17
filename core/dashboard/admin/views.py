from django.views.generic import TemplateView, UpdateView, ListView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from accounts.models import UserType
from ..permissions import HasAdminAccesPermission
from django.contrib.auth import views as auth_view
from .forms import AdminPasswordChangeForm, AdminProfileEditForm, AdminProductEditForm
from accounts.models import Profile
from shop.models import Product, Category, ProductStatus
from django.db.models import Q
from order.models import Order
from django.core.paginator import Paginator
from accounts.models import User
# -------------------------------------------------------------------------------------------  
class AdminDashboardHomeView(LoginRequiredMixin,HasAdminAccesPermission, TemplateView):
    template_name = 'dashboard/admin/home.html'
    
    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         if request.user.type != UserType.ADMIN.value:
    #             return redirect(reverse_lazy('dashboard:home'))
    #     return super().dispatch(request, *args, **kwargs)

# -----------------------------------------------------------------------------------------

class AdminSecurityEditView(LoginRequiredMixin, HasAdminAccesPermission, auth_view.PasswordChangeView):   
    template_name = 'dashboard/admin/security_edit.html'
    success_url = reverse_lazy('dashboard:admin:security-edit')
    form_class = AdminPasswordChangeForm
    
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
class AdminProfileEditView(LoginRequiredMixin, HasAdminAccesPermission, UpdateView):
    template_name = 'dashboard/admin/profile_edit.html'
    success_url = reverse_lazy('dashboard:admin:profile-edit')
    form_class = AdminProfileEditForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'پروفایل شما با موفقیت به‌روزرسانی شد.')
        return response
    
    def get_object(self, queryset=None):
        # اگر Profile وجود نداشت، یک جدید ایجاد کن
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
# -------------------------------------------------------------------------------------------  
class AdminProfileImageEditView(LoginRequiredMixin, HasAdminAccesPermission, UpdateView):
    http_method_names = ["post"]
    success_url = reverse_lazy('dashboard:admin:profile-edit')
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
class AdminProductListView(LoginRequiredMixin, HasAdminAccesPermission, ListView):
    template_name = 'dashboard/admin/product_list.html'
    context_object_name = "products"
    paginate_by = 9

    def get_paginate_by(self, queryset):
        """
        Get the number of items per page from request parameters.
        Default is 9, can be 5, 9, 12, 15, or 20.
        """
        paginate_by = self.request.GET.get('paginate_by')
        if paginate_by:
            try:
                paginate_by = int(paginate_by)
                if paginate_by in [5, 9, 12, 15, 20]:
                    return paginate_by
            except (ValueError, TypeError):
                pass
        return self.paginate_by

    def get_queryset(self):
        queryset = Product.objects.all().prefetch_related('images', 'category')
        
        # Search filter
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__icontains=search)) # | Q(description__icontains=search))
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__id=category)
        
        # Sorting
        sort = self.request.GET.get('sort')
        if sort == 'newest':
            queryset = queryset.order_by('-id')
        elif sort == 'oldest':
            queryset = queryset.order_by('id')
        elif sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort == 'name_desc':
            queryset = queryset.order_by('-name')
        else:
            queryset = queryset.order_by('-id')  # Default: newest first
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
# -------------------------------------------------------------------------------------------  
class AdminProductUpdateView(LoginRequiredMixin, HasAdminAccesPermission, UpdateView):
    template_name = 'dashboard/admin/product_update.html'
    model = Product
    form_class = AdminProductEditForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'محصول با موفقیت به‌روزرسانی شد.')
        return response

    def form_invalid(self, form):
        # نمایش خطاهای form از طریق messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product-update', kwargs={'pk': self.object.pk})
# -------------------------------------------------------------------------------------------  
class AdminProductDeleteView(LoginRequiredMixin, HasAdminAccesPermission, DeleteView):
    template_name = 'dashboard/admin/product_delete.html'
    model = Product
    
    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product-list')

    def post(self, request, *args, **kwargs):
        # Get object before deletion
        self.object = self.get_object()
        object_name = self.object.name
        
        # Delete it
        response = super().post(request, *args, **kwargs)
        
        # Add success message AFTER deletion but before redirect
        messages.success(request, f'محصول "{object_name}" با موفقیت حذف شد.')
        
        return response
# -------------------------------------------------------------------------------------------  
class AdminProductCreateView(LoginRequiredMixin, HasAdminAccesPermission, CreateView):
    template_name = 'dashboard/admin/product_create.html'
    model = Product
    form_class = AdminProductEditForm

    def form_valid(self, form):
        # Set the user as the current logged-in user
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'محصول با موفقیت ایجاد شد.')
        return response

    def form_invalid(self, form):
        # نمایش خطاهای form از طریق messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product-update', kwargs={'pk': self.object.pk})
# -------------------------------------------------------------------------------------------  
class AdminOrderListView(LoginRequiredMixin, HasAdminAccesPermission, TemplateView):
    template_name = 'dashboard/admin/orders/order_list.html'
    # context_object_name = "orders"
    # paginate_by = 10

    # def get_queryset(self):
    #     return Order.objects.all().select_related('user', 'address').prefetch_related('items__product').order_by('-created_at')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get search query
        search_query = self.request.GET.get('q', '').strip()
        context['search_query'] = search_query

        all_orders = Order.objects.all().select_related('user', 'address').prefetch_related('items__product').order_by('-created_at')
        
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
# -------------------------------------------------------------------------------------------  
class AdminOrderDetailView(LoginRequiredMixin, HasAdminAccesPermission, TemplateView):
    template_name = 'dashboard/admin/orders/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('pk')
        context['order'] = Order.objects.filter(id=order_id).select_related('user', 'address').prefetch_related('items__product').first()
        return context
# -------------------------------------------------------------------------------------------  
class AdminUserListView(LoginRequiredMixin, HasAdminAccesPermission, TemplateView):
    template_name = 'dashboard/admin/users/user_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get search query
        search_query = self.request.GET.get('q', '').strip()
        context['search_query'] = search_query

        users = User.objects.filter(type=UserType.CUSTOMER.value).select_related('user_profile').order_by('-created_date')
        
        if search_query:
            users = users.filter(
                Q(email__icontains=search_query) |
                Q(user_profile__first_name__icontains=search_query) |
                Q(user_profile__last_name__icontains=search_query)
            ).distinct()
        
        # Pagination
        paginator = Paginator(users, 10)
        page = self.request.GET.get('page', 1)
        context['users'] = paginator.get_page(page)
        context['paginator'] = paginator
        
        return context
# -------------------------------------------------------------------------------------------  

