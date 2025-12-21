from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from accounts.models import UserType
from ..permissions import HasCustomerAccesPermission
from django.contrib.auth import views as auth_view
from .forms import CustomerPasswordChangeForm,CustomerProfileEditForm
from accounts.models import Profile

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
