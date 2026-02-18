from django.urls import path,include
# from .views import SessionCartAddProduct, SessionCartRemoveProduct, SessionCart, SessionCartUpdateProduct
from . import views
app_name = 'customer'

urlpatterns = [
    path('home/',views.CustomerDashboardHomeView.as_view(), name='home'),
    path('security/edit/',views.CustomerSecurityEditView.as_view(), name='security-edit'),
    path('profile/edit/',views.CustomerProfileEditView.as_view(), name='profile-edit'),
    path('profile/image/edit/',views.CustomerProfileImageEditView.as_view(), name='profile-image-edit'),

    path('address/list/', views.CustomerAddressListView.as_view(), name='address-list'),
    path('address/create/', views.CustomerAddressCreateView.as_view(), name='address-create'),
    path('address/edit/<int:pk>/', views.CustomerAddressEditView.as_view(), name='address-edit'),
    path('address/delete/<int:pk>/', views.CustomerAddressDeleteView.as_view(), name='address-delete'),

    path('order/list/', views.CustomerOrderListView.as_view(), name='order-list'),
    path('order/detail/<int:pk>/', views.CustomerOrderDetailView.as_view(), name='order-detail'),

    path('wishlist/', views.CustomerWishlistView.as_view(), name='wishlist'),
    path('wishlist/remove/<int:pk>/', views.CustomerWishlistRemoveView.as_view(), name='wishlist-remove'),

]