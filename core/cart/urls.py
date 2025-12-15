from django.urls import path, re_path
from .views import SessionCartAddProduct, SessionCartRemoveProduct, SessionCart, SessionCartUpdateProduct

app_name = 'cart'

urlpatterns = [
    # path("session/add-product/",SessionCartAddProduct.as_view(), name="session_cart_add_product"),
    path("add/", SessionCartAddProduct.as_view(), name="add_product"),
    path("remove/", SessionCartRemoveProduct.as_view(), name="remove_product"),
    path("update/", SessionCartUpdateProduct.as_view(), name="update_product"),
    path("view-cart/",SessionCart.as_view(), name="view-cart"),
]