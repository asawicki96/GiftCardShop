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
        
        self._orders = None
        self._paid_orders = None
        self._sold_giftcards = None
        self.total_value = None
        self.total_price = None
        self.sold_giftcards_number = None
        self.income = None

    @staticmethod
    def generate_raport_data(start_date, end_date, brand): 
        ''' Generate complete Raport object containing data such as:
                total_value,
                total_price,
                sold_giftcards_number,
                income.
            params:
                start_date -- datetime.date,
                end_date -- datetime.date,
                brand -- Brand object'''

        # Initialising Raport instance 
        raport = Raport(start_date, end_date, brand)

        # Filtering orders by creation date 
        raport.orders = raport.__get_orders(raport.start_date, raport.end_date)

        # Filtering orders by related Payment objects paid status
        raport.paid_orders = raport.__get_paid_orders(raport.orders)

        # Filtering GiftCard object by Brand
        raport.sold_giftcards = raport.__get_sold_giftcards(raport.paid_orders, raport.brand)

        # Calculating total value
        raport.total_value = raport.__get_total_value(raport.sold_giftcards)

        # Calculating total price
        raport.total_price = raport.__get_total_price(raport.sold_giftcards)

        # Counting sold giftcards
        raport.sold_giftcards_number = raport.__get_sold_giftcards_number(raport.sold_giftcards)

        # Calculating income
        raport.income = raport.__get_income(raport.total_price)
        
        return raport

    
    def __get_orders(self, start_date, end_date):
        orders = Order.objects.filter(created__gte=start_date).filter(created__lte=end_date)
        if not orders:
            return None
      
        return orders

    
    def __get_paid_orders(self, orders):
        if not orders:
            return None

        for order in orders:
            payment = Payment.objects.filter(order=order).filter(paid=True)
            if not payment:
                orders = orders.exclude(pk=order.id)
        
        return orders

    
    def __get_sold_giftcards(self, paid_orders, brand):
        if not paid_orders:
            return None

        sold_giftcards = []

        for order in paid_orders:
            items = GiftCard.objects.filter(order=order).filter(brand=brand)
            for item in items:
                sold_giftcards.append(item)

        return sold_giftcards

    
    def __get_total_value(self, sold_giftcards):
        if not sold_giftcards:
            return 0
        return sum(giftcard.value for giftcard in sold_giftcards)

    
    def __get_total_price(self, sold_giftcards):
        if not sold_giftcards:
            return 0
        return sum(giftcard.price for giftcard in sold_giftcards)

    
    def __get_sold_giftcards_number(self, sold_giftcards):
        if not sold_giftcards:
            return 0
        return len(sold_giftcards)

    
    def __get_income(self, total_price):
        if total_price == 0:
            return 0
        return round((total_price * Decimal.from_float(settings.COMMISSION)), 2)



class RaportSet(object):
    def __init__(self, raports):
        self.raports = raports
        self.total_value = None
        self.total_price = None
        self.sold_giftcards_number = None
        self.total_income = None

        try:
            self.__calculate_totals()
        except Exception:
            pass

    def __calculate_totals(self):
        self.total_value = self.__get_total_value(self.raports)
        self.total_price = self.__get_total_price(self.raports)
        self.sold_giftcards_number = self.__get_sold_giftcards_number(self.raports)
        self.total_income = self.__get_income(self.raports)


    def __get_total_price(self, raports):
        return sum(raport.total_price for raport in raports)

    def __get_total_value(self, raports):
        return sum(raport.total_value for raport in raports)

    def __get_sold_giftcards_number(self, raports):
        return sum(raport.sold_giftcards_number for raport in raports)

    def __get_income(self, raports):
        return sum(raport.income for raport in raports)


class RaportFactory(object):
    @staticmethod
    def get_raport_set(start_date, end_date, brands):

        ''' Create RaportSet object containing 
            bunch of Raport objects & its totals'''

        raports = RaportFactory.__create_raports(start_date, end_date, brands)

        raport_set = RaportSet(
            raports = raports
        )

        return raport_set

    @staticmethod
    def __create_raports(start_date, end_date, brands):
        if not brands:
            return None
        
        raports = []

        for brand in brands:
            raports.append(Raport.generate_raport_data(start_date, end_date, brand))
            
        return raports      

class RaportCsvExporter(object):
    @staticmethod
    def export(raport_set: RaportSet):
        if not isinstance(raport_set, RaportSet):
            raise Exception("raport_set parameter must be an RaportSet instance")
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Raport:from_date-{}_to_date-{}"'\
            .format(raport_set.raports[0].start_date, raport_set.raports[0].end_date)
        writer = csv.writer(response)

        writer.writerow(
            [
                'Brand name', 
                'From Date', 
                'To Date', 
                'Total price', 
                'Total value', 
                'Total sold giftcards', 
                'Total income'
                ]
            )
        
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