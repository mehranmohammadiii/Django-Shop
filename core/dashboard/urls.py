from django.urls import path,include
# from .views import SessionCartAddProduct, SessionCartRemoveProduct, SessionCart, SessionCartUpdateProduct
from . import views
app_name = 'dashboard'

urlpatterns = [
    path('home/',views.DashboardHomeView.as_view(), name='home'),
    path('admin/',include('dashboard.admin.urls')),
    path('customer/',include('dashboard.customer.urls')),
    # path('')

]