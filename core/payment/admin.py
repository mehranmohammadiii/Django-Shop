from django.contrib import admin
from .models import Payment

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'status', 'authority_code', 'ref_id','response_code')

admin.site.register(Payment, PaymentAdmin)