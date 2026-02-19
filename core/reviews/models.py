from django.db import models
from shop.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
# --------------------------------------------------------------------------------------------
class ReviewStatusType(models.IntegerChoices):
    PENDING = 1, 'در انتظار بررسی'
    APPROVED = 2, 'تایید شده'
    REJECTED = 3, 'رد شده'
# --------------------------------------------------------------------------------------------
class Review(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    status = models.IntegerField(choices=ReviewStatusType.choices, default=ReviewStatusType.PENDING.value)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.email}"
# --------------------------------------------------------------------------------------------
@receiver(post_save, sender=Review)
def calculate_avg_rating(sender, instance, created, **kwargs):

    '''
    Signal creation: When a review status changes, the product's average rating is updated.
    '''

    # Review.objects.filter(product=instance.product, status=ReviewStatusType.APPROVED.value).aggregate(models.Avg('rating'))['rating__avg'] # 1

    if instance.status == ReviewStatusType.APPROVED.value:                                                                                   # 2
        product = instance.product
        approved_reviews = product.reviews.filter(status=ReviewStatusType.APPROVED.value)
        avg_rating = approved_reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
        product.avg_rating = avg_rating
        product.save()
# --------------------------------------------------------------------------------------------
