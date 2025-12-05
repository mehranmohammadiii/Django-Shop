from django.contrib.auth import forms as auth_forms
from django import forms
class AuthenticationForm(auth_forms.AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def confirm_login_allowed(self, user):
        # حالا بدون تایید هم کار می‌کنه
        return super().confirm_login_allowed(user)
