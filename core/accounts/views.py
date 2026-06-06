from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import views
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import (
    AuthenticationForm,
    SignupCompleteForm,
    SignupEmailForm,
    SignupVerifyForm,
)
from .models import User, UserType
from .services.otp import (
    clear_signup_state,
    is_email_verified,
    issue_otp,
    mark_email_verified,
)
from .tasks import send_verification_email
# -----------------------------------------------------------------------------------------------------
class HomePageView(TemplateView):
    template_name = "accounts/home.html"
# -----------------------------------------------------------------------------------------------------
class LoginView(views.LoginView):
    """
    The LoginView class is used to manage user logins.

    This view inherits from the Django LoginView class and has the following settings:
    - template_name: The name of the template in which the login form is displayed
    - form_class: The authentication form used for login (AuthenticationForm)
    - redirect_authenticated_user: If True, logged in users will be redirected to the home page
    and will not be able to access the login page again
    """

    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    # success_url = reverse_lazy('accounts:account')

   # --------------------- 
    def form_valid(self, form):
        messages.success(self.request, 'خوش‌آمدید! با موفقیت وارد شدید.')
        return super().form_valid(form)
# -----------------------------------------------------------------------------------------------------
class LogoutView(views.LogoutView):
    """
    The LogoutView class is used to manage user logouts.

    This view inherits from the Django LogoutView class and has the following settings:
    - next_page: The URL to redirect to after logout
    """
    # next_page = reverse_lazy('accounts:account')  
    next_page = '/'  # Redirect to home page after logout
    # ---------------------
    def dispatch(self, request, *args, **kwargs):

        ''''
        This method is used to dispatch the logout view.
        It displays a success message and redirects to the home page after logout.
        '''
        messages.success(request, 'با موفقیت از سیستم خارج شدید.')
        return super().dispatch(request, *args, **kwargs)
# -----------------------------------------------------------------------------------------------------
class _SignupFlowMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
# -----------------------------------------------------------------------------------------------------
class SignupEmailView(_SignupFlowMixin, FormView):

    """
    Step 1 Registration: Receive email, store OTP in Redis, send email with Celery.
    """

    template_name = "accounts/signup_email.html"
    form_class = SignupEmailForm
    success_url = reverse_lazy('accounts:signup_verify')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        code = issue_otp(email)
        send_verification_email.delay(email, code)
        self.request.session['signup_email'] = email
        messages.success(
            self.request,
            'کد تأیید به ایمیل شما ارسال شد. لطفاً صندوق ورودی را بررسی کنید.',
        )
        return super().form_valid(form)
# -----------------------------------------------------------------------------------------------------
class SignupVerifyView(_SignupFlowMixin, FormView):

    """
    Step 2 Registration: Verify OTP code from session
    """

    template_name = "accounts/signup_verify.html"
    form_class = SignupVerifyForm
    success_url = reverse_lazy('accounts:signup_complete')

    # -------------------------------------
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('signup_email'):
            messages.warning(request, 'ابتدا ایمیل خود را وارد کنید.')
            return redirect('accounts:signup')
        return super().dispatch(request, *args, **kwargs)

    # -------------------------------------
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['email'] = self.request.session['signup_email']
        return kwargs

    # -------------------------------------
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signup_email'] = self.request.session['signup_email']
        return context

    # -------------------------------------
    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'resend':
            return self._resend_code(request)
        return super().post(request, *args, **kwargs)

    # -------------------------------------
    def _resend_code(self, request):
        email = request.session.get('signup_email')
        if not email:
            messages.warning(request, 'ابتدا ایمیل خود را وارد کنید.')
            return redirect('accounts:signup')
        try:
            code = issue_otp(email)
        except ValidationError as exc:
            messages.error(request, exc.messages[0])
            return redirect('accounts:signup_verify')
        send_verification_email.delay(email, code)
        messages.success(request, 'کد جدید به ایمیل شما ارسال شد.')
        return redirect('accounts:signup_verify')

    # -------------------------------------
    def form_valid(self, form):
        email = self.request.session['signup_email']
        mark_email_verified(email)
        messages.success(self.request, 'ایمیل شما تأیید شد. رمز عبور خود را انتخاب کنید.')
        return super().form_valid(form)
# -----------------------------------------------------------------------------------------------------
class SignupCompleteView(_SignupFlowMixin, FormView):

    """
    Step 3 Registration: Choose a password, create a user, and log in automatically.
    """

    template_name = "accounts/signup_complete.html"
    form_class = SignupCompleteForm
    success_url = settings.LOGIN_REDIRECT_URL

    # -------------------------------------
    def dispatch(self, request, *args, **kwargs):
        email = request.session.get('signup_email')
        if not email:
            messages.warning(request, 'ابتدا ایمیل خود را وارد کنید.')
            return redirect('accounts:signup')
        if not is_email_verified(email):
            messages.warning(request, 'ابتدا کد تأیید ایمیل را وارد کنید.')
            return redirect('accounts:signup_verify')
        return super().dispatch(request, *args, **kwargs)

    # -------------------------------------
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['email'] = self.request.session['signup_email']
        return kwargs

    # -------------------------------------
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signup_email'] = self.request.session['signup_email']
        return context
        
    # -------------------------------------
    def form_valid(self, form):
        email = self.request.session['signup_email']
        user = User.objects.create_user(
            email=email,
            password=form.cleaned_data['password1'],
            is_verified=True,
            type=UserType.CUSTOMER,
        )
        auth.login(self.request, user)
        self.request.session.pop('signup_email', None)
        clear_signup_state(email)
        messages.success(
            self.request,
            'ثبت‌نام با موفقیت انجام شد. خوش آمدید!',
        )
        return super().form_valid(form)
# -----------------------------------------------------------------------------------------------------
