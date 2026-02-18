from django.urls import path, re_path
from .views import ShopProductListView ,ShopProductDetailView, AddOrRemoveWishlistView

app_name = 'shop'

urlpatterns = [
    path('products/list/', ShopProductListView.as_view(), name='product_list'),
    re_path(r'^products/detail/(?P<slug>[\w\-\u0600-\u06FF]+)/$', ShopProductDetailView.as_view(), name='product_detail'),
    path('add-or-remove-wishlist/<int:product_id>/', AddOrRemoveWishlistView.as_view(), name='add_or_remove_wishlist'),
]