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

    @staticmethod
    def generate_raport_data(start_date, end_date, brand):
        # Initialising Raport instance 
        raport = Raport(start_date, end_date, brand)

        # Filtering orders by creation date 
        raport.orders = Raport.get_orders(raport.start_date, raport.end_date)

        # Filtering orders by related Payment objects paid status
        raport.paid_orders = Raport.get_paid_orders(raport.orders)

        # Filtering GiftCard object by Brand
        raport.sold_giftcards = Raport.get_sold_giftcards(raport.paid_orders, raport.brand)

        # Calculating total value
        raport.total_value = Raport.get_total_value(raport.sold_giftcards)

        # Calculating total price
        raport.total_price = Raport.get_total_price(raport.sold_giftcards)

        # Counting sold giftcards
        raport.sold_giftcards_number = Raport.get_sold_giftcards_number(raport.sold_giftcards)

        #Calculating income
        raport.income = Raport.get_income(raport.total_price)
        
        return raport

    @staticmethod
    def get_orders(start_date, end_date):
        orders = Order.objects.filter(created__gte=start_date).filter(created__lte=end_date)
        if not orders:
            return None
      
        return orders

    @staticmethod
    def get_paid_orders(orders):
        if not orders:
            return None

        for order in orders:
            payment = Payment.objects.filter(order=order).filter(paid=True)
            if not payment:
                orders = orders.exclude(pk=order.id)
        
        return orders

    @staticmethod
    def get_sold_giftcards(paid_orders, brand):
        if not paid_orders:
            return None

        sold_giftcards = []

        for order in paid_orders:
            items = GiftCard.objects.filter(order=order).filter(brand=brand)
            for item in items:
                sold_giftcards.append(item)

        return sold_giftcards

    @staticmethod
    def get_total_value(sold_giftcards):
        if not sold_giftcards:
            return 0
        return sum(giftcard.value for giftcard in sold_giftcards)

    @staticmethod
    def get_total_price(sold_giftcards):
        if not sold_giftcards:
            return 0
        return sum(giftcard.price for giftcard in sold_giftcards)

    @staticmethod
    def get_sold_giftcards_number(sold_giftcards):
        if not sold_giftcards:
            return 0
        return len(sold_giftcards)

    @staticmethod
    def get_income(total_price):
        if total_price == 0:
            return 0
        return round((total_price * Decimal.from_float(settings.COMMISSION)), 2)



class RaportSet(object):
    def __init__(
        self,
        brands, 
        start_date, 
        end_date, 
        raports, 
        total_value=None, 
        total_price=None, 
        sold_giftcards_number=None, 
        total_income=None):

        self.brands = brands
        self.start_date = start_date
        self.end_date = end_date
        self.raports = raports

        self.total_value = total_value
        self.total_price = total_price
        self.sold_giftcards_number = sold_giftcards_number
        self.total_income = total_income

    def calculate_totals(self):
        self.total_value = self.get_total_value(self.raports)
        self.total_price = self.get_total_price(self.raports)
        self.sold_giftcards_number = self.get_sold_giftcards_number(self.raports)
        self.total_income = self.get_income(self.raports)


    def get_total_price(self, raports):
        return sum(raport.total_price for raport in raports)

    def get_total_value(self, raports):
        return sum(raport.total_value for raport in raports)

    def get_sold_giftcards_number(self, raports):
        return sum(raport.sold_giftcards_number for raport in raports)

    def get_income(self, raports):
        return sum(raport.income for raport in raports)


class RaportFactory(object):
    def __init__(self, brands, start_date, end_date):
        self.brands = brands
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def get_raport_set(brands, start_date, end_date):
        raports = RaportFactory.create_raports(brands, start_date, end_date)

        raport_set = RaportSet(
            brands = brands,
            start_date = start_date,
            end_date = end_date,
            raports = raports
        )

        raport_set.calculate_totals(raport_set.raports)

        return raport_set

    @staticmethod
    def create_raports(brands, start_date, end_date):
        if not brands:
            return None
        
        raports = []

        for brand in brands:
            raports.append(Raport.generate_raport_data(brand, start_date, end_date))
            
        return raports

            

class RaportCsvExporter(object):
    @staticmethod
    def export(raport_set: RaportSet):
        if not raport_set:
            raise Exception("RaportSet object required")
        if not isinstance(raport_set, RaportSet):
            raise Exception("raport_set parameter must be an RaportSet instance")
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Raport:from_date-{}_to_date-{}"'.format(raport_set.start_date, raport_set.end_date)
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
                raport_set.total_value, 
                raport_set.sold_giftcards_number, 
                raport_set.total_income])
        
        return response