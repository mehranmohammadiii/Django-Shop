from django.urls import path,include
# from .views import SessionCartAddProduct, SessionCartRemoveProduct, SessionCart, SessionCartUpdateProduct
from . import views
app_name = 'admin'

urlpatterns = [
    path('home/',views.DashboardHomeView.as_view(), name='home'),

]