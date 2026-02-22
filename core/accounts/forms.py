from django.contrib.auth import forms as auth_forms
from django import forms
from django.core.exceptions import ValidationError
# -------------------------------------------------------------------------------------
class AuthenticationForm(auth_forms.AuthenticationForm):

    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    # ------------------------------
    def confirm_login_allowed(self, user):
        '''
        This method allows checking whether the user account is active before logging in.
        If the account is inactive, it prevents logging in by displaying an error message.
        '''
        if not user.is_active:
            self.add_error(None, "این حساب کاربری غیرفعال است.")
            raise ValidationError("این حساب کاربری غیرفعال است.", code='inactive')
        return super().confirm_login_allowed(user)
# -------------------------------------------------------------------------------------  
