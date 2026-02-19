from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from .forms import SubmitReviewForm
from .models import Review, ReviewStatusType
from shop.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
# -------------------------------------------------------------------------------------------------
class SubmitReviewView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        form = SubmitReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            
            messages.success(request, 'نظر شما پس از بررسی تایید خواهد شد')
            product = review.product
            return redirect('shop:product_detail', slug=product.slug)
        else:
            product_id = request.POST.get('product')
            product = Product.objects.get(id=product_id)
            messages.error(request, 'خطایی در ثبت نظر رخ داد')
            return redirect('shop:product_detail', slug=product.slug)

# -------------------------------------------------------------------------------------------------
