from django.db import models

# Create your models here.

class PeymentStatusType(models.IntegerChoices):
    SUCCESS = 1, 'موفق'
    FAILED = 2, 'ناموفق'
    PENDING = 3, 'در انتظار پرداخت'

class Payment(models.Model):
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    authority_code = models.CharField(max_length=255, blank=True, null=True)
    ref_id = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(choices=PeymentStatusType.choices, default=PeymentStatusType.PENDING.value)
    response_json = models.JSONField(default=dict,blank=True, null=True) 
    response_code = models.IntegerField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - Amount: {self.amount} - Paid: {self.status}"