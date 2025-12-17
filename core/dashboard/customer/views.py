from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.models import UserType

class CustomerDashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/customer/home.html'
    
    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         if request.user.type != UserType.CUSTOMER.value:
    #             return redirect(reverse_lazy('dashboard:home'))
    #     return super().dispatch(request, *args, **kwargs)