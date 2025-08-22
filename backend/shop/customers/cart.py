from django.conf import settings
from decimal import Decimal

from shop.models import Book

class Cart(object):
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID) # try to get the cart from session
        if not cart:
        # if there was no cart in the session, create one
        # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def add(self, product: Book, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save() # saves the cart into the session
        
    def remove(self, product: Book):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Book.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def __len__(self) -> int | float:
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self) -> int | float:
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        """
        Removes all items from the cart.
        """
        for key in list(self.cart.keys()):
            del self.cart[key]
        self.save()