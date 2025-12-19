from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django import forms
from accounts.models import Profile


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