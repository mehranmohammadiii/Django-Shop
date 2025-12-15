from .cart import CartSession

def cart(request):
    """
    Context processor to make cart available in all templates.
    """

    cart_session = CartSession(request.session)
    return {
        'cart': cart_session,}
