from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .cart import CartSession

@receiver(user_logged_in)
def post_login(sender, request, user, **kwargs):
    """
    Signal handler for user login.
    """
    # You can add custom logic here, like logging or updating user status
    cart = CartSession(request.session)
    cart.sync_cart_items_from_db(user)
    print(f"User {user.email} logged in.")

@receiver(user_logged_out)
def pre_logout(sender, request, user, **kwargs):
    """
    Signal handler for user logout.
    """
    # You can add custom logic here, like logging or updating user status
    cart = CartSession(request.session)
    cart.merge_cart_items_to_db(user)
    print(f"User {user.email} logged out.")