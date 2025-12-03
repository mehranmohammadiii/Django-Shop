from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import views
from django.contrib import messages

class HomePageView(TemplateView):
    template_name = "accounts/home.html"

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
    form_class = views.AuthenticationForm
    redirect_authenticated_user = True
    # messages.success(request, 'کاربر با موفقیت ایجاد شد!')
# -----------------------------------------------------------------------------------------------------
class LogoutView(views.LogoutView):
    """
    The LogoutView class is used to manage user logouts.

    This view inherits from the Django LogoutView class and has the following settings:
    - next_page: The URL to redirect to after logout
    """

    # next_page = '/'  # Redirect to home page after logout