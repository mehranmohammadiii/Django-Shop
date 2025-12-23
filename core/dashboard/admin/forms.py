from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django import forms
from accounts.models import Profile
from shop.models import Product, Category


class AdminPasswordChangeForm(auth_forms.PasswordChangeForm):
    """
    A form that lets a user change their password by entering their old
    password with Persian error messages.
    """

    error_messages = {
        'password_incorrect': 'رمز عبور فعلی شما اشتباه است.',
        'password_mismatch': 'دو رمز عبور وارد شده با یکدیگر مطابقت ندارند.',
        'password_too_similar': 'رمز عبور جدید خیلی شبیه نام کاربری یا اطلاعات شخصی شما است.',
        'password_too_short': 'رمز عبور باید حداقل %(min_length)d کاراکتر باشد.',
        'password_entirely_numeric': 'رمز عبور نمی‌تواند فقط اعداد باشد.',
        'password_common': 'این رمز عبور خیلی ساده است.',
    }

    old_password = forms.CharField(
        label='رمز عبور فعلی',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'})
    )
    
    new_password1 = forms.CharField(
        label='رمز عبور جدید',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'})
    )
    
    new_password2 = forms.CharField(
        label='تایید رمز عبور جدید',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'})
    )
    # -----------------------------------------
    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
    # -----------------------------------------
    def clean_new_password2(self):
        """
        Validate that the two new password entries match and are not the old password.
        """
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2
# -------------------------------------------------------------------------------------------------------------------

class AdminProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'image', 'descriptions']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'descriptions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# -------------------------------------------------------------------------------------------------------------------

class AdminProductEditForm(forms.ModelForm):
    """
    فرم ویرایش محصولات برای مدیران
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'discount_price', 'stock', 'category', 'status', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام محصول را وارد کنید'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'توضیحات محصول را وارد کنید'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'قیمت بر حسب تومان',
                'step': '0.01'
            }),
            'discount_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'قیمت با تخفیف (اختیاری)',
                'step': '0.01'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'تعداد موجودی',
                'min': '0'
            }),
            'category': forms.CheckboxSelectMultiple(),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'name': 'نام محصول',
            'description': 'توضیحات',
            'price': 'قیمت',
            'discount_price': 'قیمت تخفیف شده',
            'stock': 'تعداد موجودی',
            'category': 'دسته‌بندی',
            'status': 'وضعیت',
            'image': 'تصویر محصول',
        }