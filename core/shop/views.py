from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    DeleteView
)
from django.db.models import Q
from .models import Product, ProductStatus, Category, wishlist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
import json
class ShopProductListView(ListView):
    """
    Display active products list with pagination support and filtering.

    This view displays active products with images and related categories.
    Supports filtering by price range, category, search, sorting, and custom pagination.
    """

    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 9

    def get_paginate_by(self, queryset):
        """
        Get the number of items per page from request parameters.
        Default is 9, can be 5, 9, 12, 15, or 20.
        """
        paginate_by = self.request.GET.get('paginate_by')
        if paginate_by:
            try:
                paginate_by = int(paginate_by)
                if paginate_by in [5, 9, 12, 15, 20]:
                    return paginate_by
            except (ValueError, TypeError):
                pass
        return self.paginate_by

    def get_queryset(self):
        queryset = Product.objects.filter(status=ProductStatus.ACTIVE).prefetch_related('images', 'category')
        
        # Search filter
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__icontains=search)) # | Q(description__icontains=search))
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__id=category)
        
        # Sorting
        sort = self.request.GET.get('sort')
        if sort == 'newest':
            queryset = queryset.order_by('-id')
        elif sort == 'oldest':
            queryset = queryset.order_by('id')
        elif sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort == 'name_desc':
            queryset = queryset.order_by('-name')
        else:
            queryset = queryset.order_by('-id')  # Default: newest first
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['wishlist'] = wishlist.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        context['categories'] = Category.objects.all()

        return context
# ----------------------------------------------------------------------
class ShopProductDetailView(DetailView):
    """
    Display detailed view of a single product.

    This view shows detailed information about a product, including images, category,
    and similar products from the same categories.
    """

    template_name = "shop/product_detail.html"
    context_object_name = "product"
    queryset = Product.objects.prefetch_related('images', 'category')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        product_categories = product.category.all()
        
        similar_products = Product.objects.filter(
            status=ProductStatus.ACTIVE,
            category__in=product_categories
        ).exclude(
            id=product.id
        ).prefetch_related('images', 'category').distinct()[:4]
        
        context['similar_products'] = similar_products
        return context
# ----------------------------------------------------------------------
class AddOrRemoveWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id', product_id)
        except:
            product_id = request.POST.get('product_id', product_id)
        
        product = Product.objects.get(id=product_id)
        wishlist_item, created = wishlist.objects.get_or_create(
            user=request.user, 
            product=product
        )
        
        if created:
            return JsonResponse({'status': 'added'})
        else:
            wishlist_item.delete()
            return JsonResponse({'status': 'removed'})
# ----------------------------------------------------------------------