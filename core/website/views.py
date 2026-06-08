from django.shortcuts import render
from django.views.generic import TemplateView
from shop.models import Product, ProductStatus, Category

class HomePageView(TemplateView):
    template_name = "website/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get 8 active products to display on the home page
        context['products'] = Product.objects.filter(
            status=ProductStatus.ACTIVE
        ).prefetch_related('images', 'category')[:8]

        # Get 3 products for the main slider (Hero Slider)
        context['hero_slider_products'] = Product.objects.filter(
            status=ProductStatus.ACTIVE
        ).prefetch_related('images', 'category')[:3]
        
        # Get all categories to display in the card grid
        context['categories'] = Category.objects.all()[:3]
        
        return context

class AboutPageView(TemplateView):
    template_name = "website/about.html"

class ContactPageView(TemplateView):
    template_name = "website/contact.html"