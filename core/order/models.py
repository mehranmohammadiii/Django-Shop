from django.db import models

# ---------------------------------------------------------------------------------------------------------
class OrderStatusTypes(models.IntegerChoices):
    PENDING = 1, 'Pending'
    PROCESSING = 2, 'Processing'
    SHIPPED = 3, 'Shipped'
    DELIVERED = 4, 'Delivered'
    CANCELED = 5, 'Canceled'
# ---------------------------------------------------------------------------------------------------------
class UserAddress(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    # full_name = models.CharField(max_length=255)
    # phone_number = models.CharField(max_length=20)
    # address_line2 = models.CharField(max_length=255, blank=True, null=True)
    # country = models.CharField(max_length=100)
    # is_default = models.BooleanField(default=False)

    def __str__(self):
        return f" {self.address_line1}, {self.city}" 
# ---------------------------------------------------------------------------------------------------------
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    max_limit_usage = models.PositiveIntegerField(default=10)
    used_by = models.ManyToManyField('accounts.User', related_name='used_coupons', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
# ---------------------------------------------------------------------------------------------------------
class Order(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.PROTECT)
    status = models.IntegerField(choices=OrderStatusTypes.choices, default=OrderStatusTypes.PENDING.value)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)

    def calculate_total_price(self):
        total = sum(item.price * item.quantity for item in self.items.all())
        return total
    
    def __str__(self):
        return f"Order #{self.address} by {self.user}"
# ---------------------------------------------------------------------------------------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
# ---------------------------------------------------------------------------------------------------------
