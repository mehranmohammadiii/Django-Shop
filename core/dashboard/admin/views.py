from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from accounts.models import UserType
from ..permissions import HasAdminAccesPermission
from django.contrib.auth import views as auth_view
from .forms import AdminPasswordChangeForm, AdminProfileEditForm
from accounts.models import Profile

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
