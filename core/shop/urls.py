from django.urls import path, re_path
from .views import ShopProductListView ,ShopProductDetailView

app_name = 'shop'

urlpatterns = [
    path('products/list/', ShopProductListView.as_view(), name='product_list'),
    re_path(r'^products/detail/(?P<slug>[\w\-\u0600-\u06FF]+)/$', ShopProductDetailView.as_view(), name='product_detail'),
]