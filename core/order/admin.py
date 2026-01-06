from django.contrib import admin
from .models import Order, OrderItem, Coupon, UserAddress



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at', 'coupon')
    search_fields = ('user__username', 'id')

@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'max_limit_usage', 'used_by_count', 'active', 'expiration_date')
    search_fields = ('code',)
    def used_by_count(self, obj):
        return obj.used_by.all().count()
    
@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line1', 'city', 'state', 'postal_code')
    search_fields = ('user__username', 'address_line1', 'city')
