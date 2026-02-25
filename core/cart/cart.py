from .models import CartItem, Cart
from shop.models import Product
# ----------------------------------------------------------------------------------------------
class CartSession:

    """
    A class for managing a user's shopping cart using Django Session

    This class provides the following features:
    - Add a product to the shopping cart
    - Remove a product from the shopping cart
    - Clear the entire shopping cart
    - Get the list of products in the cart
    - Calculate the total number of products

    The shopping cart data is stored in the session as a dictionary.
    """
    
    # ---------------------------------
    def __init__(self, session):

        self.session = session

        '''
        Initializes the CartSession instance.
        This constructor receives the session object and ensures that the session has
        a 'cart' key initialized as a dictionary with 'items', 'total_price', and 'total_items'.
        All cart operations will modify this session-based cart data structure.
        self.session = session
        '''

        self.cart = self.session.setdefault('cart', {
            'items':[],
            'total_price':0,
            'total_items':0
        })

    # ---------------------------------------
    def add_product(self, product_id, quantity=1):

        '''
        This method adds a product to the shopping cart in the session.
        If the product already exists in the cart, it increases its quantity by the given amount.
        Otherwise, it adds a new item for the product with the specified quantity.
        After making changes, it saves the cart state to the session.
        '''

        product_id = str(product_id)
        for item in self.cart['items']:
            if product_id == item['product_id']:
                item['quantity'] += quantity
                break
        else:
            new_item = {
                'product_id':product_id,
                'quantity':1
            }
            self.cart['items'].append(new_item)
            
        self.save()

    # ---------------------------------------
    def remove(self, product_id):
        product_id = str(product_id)
        self.cart['items'] = [item for item in self.cart['items'] if item['product_id'] != product_id]
        self.save()

    # ---------------------------------------
    def update_product(self, product_id, quantity):
        product_id = str(product_id)
        for item in self.cart['items']:
            if item['product_id'] == product_id:
                item['quantity'] = quantity
                break
        self.save()

    # ---------------------------------------
    def save(self):
        self.session.modified = True

    # ---------------------------------------
    def clear(self):
        if 'cart' in self.session:
            del self.session['cart']
        self.save()

    # ---------------------------------------
    def get_cart_items(self):
        return self.cart['items']

    # ---------------------------------------
    def get_total_items(self):
        return len(self.cart['items'])

    # ---------------------------------------
    def __iter__(self):

        """
        This method makes the CartSession class iterable. It allows for use in for loops.
        """

        return iter(self.cart['items'])

    # ---------------------------------------
    def sync_cart_items_from_db(self, user):

        """
        This method syncs the session cart items with the cart items stored in the database for a given user.
        It loads or creates the user's persistent cart, updates quantities of existing items to match the session,
        adds any new items found in the database but not in the session, and then merges all cart items back
        to the database, ensuring that the cart state remains consistent between the session and persistent storage.
        """

        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            for item in self.cart['items']:
                if str(cart_item.product.id) == item['product_id']:
                    cart_item.quantity = item['quantity']
                    cart_item.save()
                    break
            else:
                new_item = {
                'product_id':str(cart_item.product.id),
                'quantity':cart_item.quantity
            }
                self.cart['items'].append(new_item)
        self.merge_cart_items_to_db(user)
        self.save()

    # ---------------------------------------
    def merge_cart_items_to_db(self, user):

        """
        This method merges the session cart items with the user's persistent cart in the database.
        For each item in the session cart, it either updates the quantity of the existing CartItem
        or creates a new one associated with the user's cart. Afterward, it removes any CartItems
        from the database that are not present in the session cart, ensuring both carts remain in sync.
        """

        cart, created = Cart.objects.get_or_create(user=user)
        for item in self.cart['items']:
            product_obj = Product.objects.get(id=item['product_id'])
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product_obj)
            cart_item.quantity = item['quantity']
            cart_item.save()
        session_product_ids = [item['product_id'] for item in self.cart['items']]
        CartItem.objects.filter(cart=cart).exclude(product__id__in=session_product_ids).delete()
# -----------------------------------------------------------------------------------------------------------------------
