from django.contrib.auth import forms as auth_forms, password_validation
from django import forms
from django.core.exceptions import ValidationError

from .models import User
from .services.otp import check_rate_limit, is_email_verified, verify_otp
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
class SignupEmailForm(forms.Form):
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-lg text-center',
                'placeholder': 'email@site.com',
                'autofocus': True,
            }
        ),
    )
    # -------------------------------------
    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("این ایمیل قبلاً ثبت شده است.")
        check_rate_limit(email)
        return email
# -------------------------------------------------------------------------------------
class SignupVerifyForm(forms.Form):

    code = forms.CharField(
        label="کد تأیید",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg text-center',
                'placeholder': '123456',
                'autofocus': True,
                'inputmode': 'numeric',
                'autocomplete': 'one-time-code',
            }
        ),
    )

    # -------------------------------------
    def __init__(self, email, *args, **kwargs):
        self.email = email
        super().__init__(*args, **kwargs)

    # -------------------------------------
    def clean_code(self):
        code = self.cleaned_data['code'].strip()
        if not code.isdigit():
            raise ValidationError("کد باید ۶ رقم باشد.")
        if not verify_otp(self.email, code):
            raise ValidationError("کد نامعتبر یا منقضی شده است.")
        return code
# -------------------------------------------------------------------------------------
class SignupCompleteForm(forms.Form):
    password1 = forms.CharField(
        label="رمز عبور",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg text-center', 'autofocus': True},
        ),
    )
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg text-center'},
        ),
    )

    def __init__(self, email, *args, **kwargs):
        self.email = email
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not is_email_verified(self.email):
            raise ValidationError("ایمیل تأیید نشده است. لطفاً دوباره کد را وارد کنید.")
        if User.objects.filter(email__iexact=self.email).exists():
            raise ValidationError("این ایمیل قبلاً ثبت شده است.")
        return cleaned_data

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("رمزهای عبور مطابقت ندارند.")
        if password2:
            password_validation.validate_password(
                password2,
                user=User(email=self.email),
            )
        return password2
# -------------------------------------------------------------------------------------  
