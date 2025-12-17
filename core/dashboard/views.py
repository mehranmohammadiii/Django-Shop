from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.models import UserType

class DashboardHomeView(LoginRequiredMixin, View):
    
    # template_name = 'dashboard/home.html'
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['user_type'] = self.request.user.type
    #     return context
    
    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            if request.user.type == UserType.CUSTOMER.value:
                return redirect(reverse_lazy('dashboard:customer:home'))
            if request.user.type == UserType.ADMIN.value:
                return redirect(reverse_lazy('dashboard:admin:home'))
            
        else:
            return redirect(reverse_lazy('accounts:login'))
        return super().dispatch(request, *args, **kwargs)