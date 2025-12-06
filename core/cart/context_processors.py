from .cart import CartSession

def cart(request):
    """
    Context processor to make cart available in all templates.
    """
    # user_cart = None
    # cart_items_count = 0
    
    # if request.user.is_authenticated:
    #     user_cart, created = Cart.objects.get_or_create(user=request.user)
    #     cart_items_count = user_cart.items.count()
    
    # return {
    #     'cart': user_cart,
    #     'cart_items_count': cart_items_count,
    #     'test' : 'hello world'
    # }
    cart_session = CartSession(request.session)
    return {
        'cart': cart_session,}
