from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .cart import CartSession
# ----------------------------------------------------------------------------------------------
@receiver(user_logged_in)
def post_login(sender, request, user, **kwargs):

    """
    Signal handler for user login.
    This function is called after a user successfully logs in.
    It is responsible for syncing the shopping cart stored in the session 
    with the cart items stored in the database for the logged-in user,
    ensuring cart data consistency between session and persistent storage.
    """
    
    cart = CartSession(request.session)
    cart.sync_cart_items_from_db(user)
    print(f"User {user.email} logged in.")

# ----------------------------------------------------------------------------------------------
@receiver(user_logged_out)
def pre_logout(sender, request, user, **kwargs):

    """
    Signal handler for user logout.
    This function is called before a user logs out of the system.
    It ensures that any changes made to the shopping cart while the user was logged in 
    (e.g., adding or removing items) are persisted in the database by merging the current 
    session cart with the database cart. This keeps cart data consistent across user sessions.
    """

    cart = CartSession(request.session)
    cart.merge_cart_items_to_db(user)
    print(f"User {user.email} logged out.")
# ----------------------------------------------------------------------------------------------