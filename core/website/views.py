from django.shortcuts import render
from django.views.generic import TemplateView
from shop.models import Product, ProductStatus

class HomePageView(TemplateView):
    template_name = "website/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # دریافت 8 محصول فعال برای نمایش در صفحه اصلی
        context['products'] = Product.objects.filter(
            status=ProductStatus.ACTIVE
        ).prefetch_related('images', 'category')[:8]
        return context

class AboutPageView(TemplateView):
    template_name = "website/about.html"

class ContactPageView(TemplateView):
    template_name = "website/contact.html"