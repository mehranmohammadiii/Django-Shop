from django.contrib import admin
from .models import Product, Category, ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'created_at')
    search_fields = ('product__name', 'alt_text')

admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Product, ProductAdmin)

