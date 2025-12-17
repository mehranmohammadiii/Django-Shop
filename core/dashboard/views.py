from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.models import UserType

class DashboardHomeView(View,LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            if request.user.type == UserType.CUSTOMER.value:
                return redirect(reverse_lazy('#'))
            if request.user.type == UserType.ADMIN.value:
                return redirect(reverse_lazy('#'))
            

            
        else:
            return redirect(reverse_lazy('accounts:login'))
        return super().dispatch(request, *args, **kwargs)