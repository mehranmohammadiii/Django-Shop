from django.urls import path
from .views import HomePageView , LoginView , LogoutView

app_name = 'accounts'

urlpatterns = [
    path('', HomePageView.as_view(), name='account'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]