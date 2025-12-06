from django.urls import path, re_path
from .views import SessionCartAddProduct

app_name = 'cart'

urlpatterns = [
    path("session/add-product/",SessionCartAddProduct.as_view(), name="session_cart_add_product"),
    path("add/", SessionCartAddProduct.as_view(), name="add_product"),
]