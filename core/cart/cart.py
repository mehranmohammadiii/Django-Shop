class CartSession :
    def __init__(self, session):
        self.session = session

        self.cart = self.session.setdefault('cart', {
            'items':[],
            'total_price':0,
            'total_items':0
        })


    def add_product(self, product_id, quantity=1):
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

    def remove(self, product_id):
        product_id = str(product_id)
        self.cart['items'] = [item for item in self.cart['items'] if item['product_id'] != product_id]
        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        if 'cart' in self.session:
            del self.session['cart']
        self.save()
    def get_cart_items(self):
        return self.cart['items']

    def get_total_items(self):
        return sum(item['quantity'] for item in self.cart['items'])