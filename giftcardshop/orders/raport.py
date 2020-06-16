from .models import Order
from giftcards.models import GiftCard
from payments.models import Payment
from django.conf import settings
from decimal import Decimal

class Raport(object):
    def __init__(self, start_date=None, end_date=None, brand=None):
        self.brand = brand
        self.start_date = start_date
        self.end_date = end_date
        
        self.orders = None
        self.paid_orders = None
        self.sold_giftcards = None
        self.total_value = None
        self.total_price = None
        self.sold_giftcards_number = None
        self.income = None

    def generate_raport_data(self):
        self.orders = self.get_orders(self.start_date, self.end_date, self.brand)
        self.paid_orders = self.get_paid_orders(self.orders)
        self.sold_giftcards = self.get_sold_giftcards(self.paid_orders, self.brand)
        self.total_value = self.get_total_value(self.sold_giftcards)
        self.total_price = self.get_total_price(self.sold_giftcards)
        self.sold_giftcards_number = self.get_sold_giftcards_number(self.sold_giftcards)
        self.income = self.get_income(self.total_price)
        
        return self

    def get_orders(self, start_date, end_date, brand):
        orders = Order.objects.filter(created__gte=start_date).filter(created__lte=end_date)
      
        return orders

    def get_paid_orders(self, orders):
        print(orders)
        if not orders:
            return None

        for order in orders:
            payment = Payment.objects.filter(order=order).filter(paid=True)
            if not payment:
                orders = orders.exclude(pk=order.id)
        
        return orders

    def get_sold_giftcards(self, paid_orders, brand):
        if not paid_orders:
            return None

        sold_giftcards = []

        for order in paid_orders:
            items = GiftCard.objects.filter(order=order).filter(brand=brand)
            for item in items:
                sold_giftcards.append(item)

        return sold_giftcards

    def get_total_value(self, sold_giftcards):
        return sum(giftcard.value for giftcard in sold_giftcards)

    def get_total_price(self, sold_giftcards):
        return sum(giftcard.price for giftcard in sold_giftcards)

    def get_sold_giftcards_number(self, sold_giftcards):
        return len(sold_giftcards)

    def get_income(self, total_price):
        return round((total_price * Decimal.from_float(settings.COMMISSION)), 2)

