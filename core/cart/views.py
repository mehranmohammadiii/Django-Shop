from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from .cart import CartSession

class SessionCartAddProduct(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if not product_id:
            return JsonResponse({'status': 'error', 'message': 'product_id is required'}, status=400)
        
        cart = CartSession(request.session)
        cart.add_product(product_id, quantity)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product added to cart',
            'cart_items': cart.get_cart_items(),
            'total_items': cart.get_total_items()
        })