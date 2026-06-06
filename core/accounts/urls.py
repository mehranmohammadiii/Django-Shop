from django.urls import path
from .views import (
    HomePageView,
    LoginView,
    LogoutView,
    SignupEmailView,
    SignupVerifyView,
    SignupCompleteView,
)

app_name = 'accounts'

urlpatterns = [
    path('', HomePageView.as_view(), name='account'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupEmailView.as_view(), name='signup'),
    path('signup/verify/', SignupVerifyView.as_view(), name='signup_verify'),
    path('signup/complete/', SignupCompleteView.as_view(), name='signup_complete'),
]