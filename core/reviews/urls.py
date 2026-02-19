from django.urls import path, re_path
from .views import SubmitReviewView
# from .views import ShopProductListView ,ShopProductDetailView, AddOrRemoveWishlistView

app_name = 'reviews'

urlpatterns = [
        path('submit/review/', SubmitReviewView.as_view(), name='submit_review'),
]