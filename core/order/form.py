from django import forms
from .models import Coupon
from django.utils import timezone

class CheckOutForm(forms.Form):
    coupon_code = forms.CharField(
        required=False,
        max_length=50,
        label="Coupon Code",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your coupon code',
            'id': 'id_coupon_code',
            'class': 'form-control'
        })
    )
    
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
    
    def clean_coupon_code(self):
        code = self.cleaned_data.get('coupon_code')
        
        # اگر کد خالی باشد، پروانه نیست
        if not code:
            return code
            
        user = self.request.user

        coupon = None
        try:
            coupon = Coupon.objects.get(code=code, active=True)
        except Coupon.DoesNotExist:
            raise forms.ValidationError("کد تخفیف وارد شده معتبر نیست.")

        if coupon:
            if coupon.used_by.count() >= coupon.max_limit_usage:
                raise forms.ValidationError("این کد تخفیف به حد نصاب استفاده رسیده است.")
            
            if coupon.expiration_date and coupon.expiration_date < timezone.now():
                raise forms.ValidationError("این کد تخفیف منقضی شده است.")
            
            if user in coupon.used_by.all():
                raise forms.ValidationError("شما قبلا از این کد تخفیف استفاده کرده‌اید.")
            
            # ذخیره coupon برای استفاده در views
            self.coupon = coupon
        
        return code