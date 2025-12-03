from django.contrib.auth import forms

class AuthenticationForm(forms.AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def confirm_login_allowed(self, user):
        if not user.is_verified:
            raise forms.ValidationError(
                ("This account is not verified."),
                code='unverified',
            )
        return super().confirm_login_allowed(user)
