from django.urls import path, re_path
from .views import CheckoutView, CompletedView, validate_coupon, FailedView

app_name = 'order'

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path('complete/', CompletedView.as_view(), name='checkout-complete'),
    path('failed/', FailedView.as_view(), name='checkout-failed'),
    path('validate-coupon/', validate_coupon.as_view(), name='validate-coupon'),

]