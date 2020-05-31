from decimal import Decimal
from django.conf import settings
from giftcards.models import GiftCard

class Cart(object):
    def __init__(self, request):
        cart = request.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = request.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def add(self, request, giftcard):
        giftcard_id = str(giftcard.id)
        if giftcard_id not in self.cart:
            self.cart[giftcard_id] = {'price': str(giftcard.purchase_amount)}
        self.save(request)

    def remove(self, request, giftcard):
        giftcard_id = str(giftcard.id)
        if giftcard_id in self.cart:
            del self.cart[giftcard_id]
            self.save(request)

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

    def save(self, request):
        request.session[settings.CART_SESSION_ID] = self.cart
        request.session.modified = True
    
    def clear(self, request):
        del request.session[settings.CART_SESSION_ID]
        request.session.modified = True
