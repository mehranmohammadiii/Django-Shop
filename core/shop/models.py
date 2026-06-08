from django.db import models
from django.conf import settings
from django.utils.text import slugify
# ---------------------------------------------------------------------------------------------------
class ProductStatus(models.IntegerChoices):
    ACTIVE = 1, 'Active'
    INACTIVE = 2, 'Inactive'
    OUT_OF_STOCK = 3, 'Out of Stock'
# ---------------------------------------------------------------------------------------------------
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    category = models.ManyToManyField('Category', related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    image = models.ImageField(default='/default/product-img.pg', upload_to='product/img', blank=True, null=True)
    discount_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    status = models.PositiveSmallIntegerField(choices=ProductStatus.choices, default=ProductStatus.ACTIVE)
    
    avg_rating = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    
    # ----------------------------------
    def save(self, *args, **kwargs):
        # اگر عکس تغییر کرده است، عکس‌های دیگر و ProductImage‌های قدیم را حذف کن
        if self.pk:
            try:
                old_instance = Product.objects.get(pk=self.pk)
                # اگر عکس اصلی تغییر کرده است
                if old_instance.image != self.image:
                    # عکس قدیم را حذف کن
                    if old_instance.image:
                        old_instance.image.delete(save=False)
                    # تمام ProductImage‌های قدیم را حذف کن
                    self.images.all().delete()
            except Product.DoesNotExist:
                pass
        
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    # ----------------------------------
    def __str__(self):
        return self.name
    
    # ----------------------------------
    class Meta:
        ordering = ['-created_at']
# ---------------------------------------------------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    
    # ----------------------------------
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    # ----------------------------------
    def __str__(self):
        return self.name
# ---------------------------------------------------------------------------------------------------
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product/images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # ----------------------------------
    def __str__(self):
        return f"Image for {self.product.name}"
# ---------------------------------------------------------------------------------------------------
class wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # ----------------------------------
    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']
# ---------------------------------------------------------------------------------------------------