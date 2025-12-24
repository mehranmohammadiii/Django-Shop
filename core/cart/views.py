from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from .cart import CartSession
from shop.models import Product

class SessionCartAddProduct(View):
    """
    View for adding a product to a shopping cart by session

    This class receives a POST request and:
    - Gets the product_id and quantity from the request
    - Adds the product to the session shopping cart
    - Returns the shopping cart information as JSON
    """
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if not product_id:
            return JsonResponse({'status': 'error', 'message': 'product_id is required'}, status=400)
        
        cart = CartSession(request.session)
        cart.add_product(product_id, quantity)
        
        if request.user.is_authenticated:
            cart.merge_cart_items_to_db(request.user)

        return JsonResponse({
            'status': 'success',
            'message': 'Product added to cart',
            'cart_items': cart.get_cart_items(),
            'total_items': cart.get_total_items()
        })

# -----------------------------------------------
class SessionCartRemoveProduct(View):
    """
    View for removing a product from a shopping cart by session

    This class receives a POST request and:
    - Gets the product_id from the request
    - Removes the product from the session shopping cart
    - Returns the updated shopping cart information as JSON
    """
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        
        if not product_id:
            return JsonResponse({'status': 'error', 'message': 'product_id is required'}, status=400)
        
        cart = CartSession(request.session)
        cart.remove(product_id)

        if request.user.is_authenticated:
            cart.merge_cart_items_to_db(request.user)
        return JsonResponse({
            'status': 'success',
            'message': 'Product removed from cart',
            'cart_items': cart.get_cart_items(),
            'total_items': cart.get_total_items()
        })

# -----------------------------------------------
class SessionCartUpdateProduct(View):
    """
    View for updating the quantity of a product in the shopping cart by session

    This class receives a POST request and:
    - Gets the product_id and new quantity from the request
    - Updates the product quantity in the session shopping cart
    - Returns the updated shopping cart information as JSON
    """
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if not product_id:
            return JsonResponse({'status': 'error', 'message': 'product_id is required'}, status=400)
        
        cart = CartSession(request.session)
        cart.update_product(product_id, quantity)

        if request.user.is_authenticated:
            cart.merge_cart_items_to_db(request.user) 
                  
        return JsonResponse({
            'status': 'success',
            'message': 'Product quantity updated',
            'cart_items': cart.get_cart_items(),
            'total_items': cart.get_total_items()
        })

# -----------------------------------------------
class SessionCart(TemplateView):
    """
    View for displaying the shopping cart stored in the session.

    This class renders a template showing the contents of the shopping cart
    with product details fetched from the database.
    """
    template_name = 'cart/session_cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        cart_items = cart.get_cart_items()
        
        # دریافت اطلاعات محصولات از دیتابیس
        products_dict = {}
        product_ids = [item['product_id'] for item in cart_items]
        
        if product_ids:
            products = Product.objects.filter(id__in=product_ids)
            products_dict = {str(p.id): p for p in products}       # {'25','30','49'}
        
        # ترکیب اطلاعات سبد خرید با داده‌های محصول
        cart_with_products = []
        total_price = 0
        
        for item in cart_items:
            product = products_dict.get(item['product_id'])
            if product:
                item_total = float(product.price) * item['quantity']
                total_price += item_total
                cart_with_products.append({
                    'product_id': item['product_id'],
                    'product': product,
                    'quantity': item['quantity'],
                    'item_total': item_total
                })
        
        context['cart'] = cart_with_products
        context['total_items'] = cart.get_total_items()
        context['total_price'] = total_price
        return context
# ---------------------------------------------------------------------------------------------------------------------------