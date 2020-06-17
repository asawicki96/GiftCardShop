from .models import Order
from giftcards.models import GiftCard
from payments.models import Payment
from django.conf import settings
from decimal import Decimal
from django.http import HttpResponse
import csv

class Raport(object):
    def __init__(self, start_date, end_date, brand):
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

class RaportSet(object):
    def __init__(
        self,
        brands, 
        start_date, 
        end_date, 
        raports, 
        total_value, 
        total_price, 
        sold_giftcards_number, 
        total_income):

        self.brands = brands
        self.start_date = start_date
        self.end_date = end_date

        self.raports = raports
        self.total_value = total_value
        self.total_price = total_price
        self.sold_giftcards_number = sold_giftcards_number
        self.total_income = total_income


class RaportFactory(object):
    def __init__(self, brands, start_date, end_date):
        self.brands = brands
        self.start_date = start_date
        self.end_date = end_date

    def get_raports(self):
        raports = self.create_raports(self.brands, self.start_date, self.end_date)

        raport_set = RaportSet(
            brands = self.brands,
            start_date = self.start_date,
            end_date = self.end_date,
            raports = raports,
            total_value = self.get_total_value(raports),
            total_price = self.get_total_price(raports),
            sold_giftcards_number = self.get_sold_giftcards_number(raports),
            total_income = self.get_income(raports)
        )
        
        return raport_set

    def create_raports(self, brands, start_date, end_date):
        if not brands:
            return None
        
        raports = []

        for brand in brands:
            raport = Raport(
                brand=brand, 
                start_date=start_date, 
                end_date=end_date)

            raports.append(raport.generate_raport_data())
            
        return raports

    def get_total_price(self, raports):
        return sum(raport.total_price for raport in raports)

    def get_total_value(self, raports):
        return sum(raport.total_value for raport in raports)

    def get_sold_giftcards_number(self, raports):
        return sum(raport.sold_giftcards_number for raport in raports)

    def get_income(self, raports):
        return sum(raport.income for raport in raports)
            

class RaportCsvExporter(object):
    @staticmethod
    def export(raport_set: RaportSet):
        if not raports:
            raise Exception("List of Raport objects required")
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Raport:from_date-{}_to_date-{}"'.format(raports.start_date, raports.end_date)
        writer = csv.writer(response)

        writer.writerow(['Brand name', 'From Date', 'To Date', 'Total price', 'Total value', 'Total sold giftcards', 'Total income'])
        
        for raport in raport_set.raports:
            writer.writerow([
                raport.brand, 
                raport.start_date, 
                raport.end_date, 
                raport.total_price, 
                raport.total_value, 
                raport.sold_giftcards_number, 
                raport.income])

        writer.writerow([' ', ' ', ' ', ' ', ' ', ' ', ' '])
        writer.writerow([' ', ' ', ' ', 'Total', 'Total', 'Total', 'Total'])
        writer.writerow([
                ' ', 
                ' ', 
                ' ', 
                raport_set.total_price, 
                raports_set.total_value, 
                raports_set.sold_giftcards_number, 
                raports_set.total_income])
        
        return response