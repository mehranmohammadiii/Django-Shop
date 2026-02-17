from django.urls import path,include
from . import views
app_name = 'admin'

urlpatterns = [
    path('home/',views.AdminDashboardHomeView.as_view(), name='home'),
    path('security/edit/',views.AdminSecurityEditView.as_view(), name='security-edit'),
    path('profile/edit/',views.AdminProfileEditView.as_view(), name='profile-edit'),
    path('profile/image/edit/',views.AdminProfileImageEditView.as_view(), name='profile-image-edit'),
    path('product/list/',views.AdminProductListView.as_view(), name='product-list'),
    path('product/update/<int:pk>/',views.AdminProductUpdateView.as_view(), name='product-update'),
    path('product/delete/<int:pk>/', views.AdminProductDeleteView.as_view(), name='product-delete'),
    path('product/create/', views.AdminProductCreateView.as_view(), name='product-create'),

    path('order/list/', views.AdminOrderListView.as_view(), name='order-list'),
    path('order/detail/<int:pk>/', views.AdminOrderDetailView.as_view(), name='order-detail'),

    path('user/list/', views.AdminUserListView.as_view(), name='user-list'),

]