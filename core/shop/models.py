from django.db import models
from django.conf import settings


class ProductStatus(models.IntegerChoices):
    ACTIVE = 1, 'Active'
    INACTIVE = 2, 'Inactive'
    OUT_OF_STOCK = 3, 'Out of Stock'
# ---------------------------------------------------------------------------------------------------
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    image = models.ImageField(default='/default/product-img.pg', upload_to='product/img', blank=True, null=True)
    discount_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='products')
    status = models.PositiveSmallIntegerField(choices=ProductStatus.choices, default=ProductStatus.ACTIVE)
    
    avg_rating = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
# ---------------------------------------------------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    
    def __str__(self):
        return self.name
# ---------------------------------------------------------------------------------------------------
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product/images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Image for {self.product.name}"
# ---------------------------------------------------------------------------------------------------
class wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']
# ---------------------------------------------------------------------------------------------------