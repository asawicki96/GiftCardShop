from decimal import Decimal
from django.conf import settings
from giftcards.models import GiftCard

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def add(self, giftcard):
        giftcard_id = str(giftcard.id)
        if giftcard_id not in self.cart:
            self.cart[giftcard_id] = {'price': str(giftcard.purchase_amount)}
        self.save()

    def remove(self, giftcard):
        giftcard_id = str(giftcard.id)
        if giftcard_id in self.cart:
            del self.cart[giftcard_id]
            self.save()

    def __iter__(self):
        giftcards_ids = self.cart.keys()
        giftcards = GiftCard.objects.filter(id__in=giftcards_ids)

        for giftcard in giftcards:
            self.cart[str(giftcard.id)]['giftcard'] = giftcard

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.cart.values())

    def get_len(self):
        return sum(1 for item in self.cart.values())

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
