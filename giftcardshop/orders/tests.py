from django.test import TestCase
from .models import Order
from payments.models import Payment
from giftcards.models import GiftCard
from django.contrib.auth.models import User
from brands.models import Brand, Category
import datetime
import decimal
from . import raport
import pytz

# Create your tests here.

utc = pytz.UTC

class RaportTestCase(TestCase):

    # TEST DATA SETUP

    def setUp(self):

        #Creating 1 User object

        User.objects.create(
            username='username', 
            password='password', 
            email='email@gmail.com', 
            first_name='user_first_name', 
            last_name='user_last_name'
            )
        
        #Creating 3 Order objects

        Order.objects.create(user=User.objects.get(pk=1), created=datetime.datetime(year=2020, month=7, day=15))
        Order.objects.create(user=User.objects.get(pk=1), created=datetime.datetime(year=2020, month=7, day=15))
        Order.objects.create(user=User.objects.get(pk=1), created=datetime.datetime(year=2020, month=6, day=15))

        #Creating Category object

        Category.objects.create(
            name='Category1',
            slug='category1',
            description='category1_description'
        )

        #Creating 2 Brand Objects associated with one Category

        b1 = Brand.objects.create(
            name='Brand1',
            slug='brand1',
            description='brand1_description'
        )
        b1.category.add(Category.objects.get(pk=1))

        b2 = Brand.objects.create(
            name='Brand2',
            slug='brand2',
            description='brand2_description'
        )
        b2.category.add(Category.objects.get(pk=1))

        
        #Creating 6 GiftCard objects;
        # 3 associated with brand1 & order1
        # 3 associated with brand2 & order2

        for i in range(3):
            GiftCard.objects.create(
                price=1.00,
                value=1.00,
                brand=Brand.objects.get(pk=1),
                order=Order.objects.get(pk=1)
            )

        for i in range(3):
            GiftCard.objects.create(
                price=1.00,
                value=1.00,
                brand=Brand.objects.get(pk=2),
                order=Order.objects.get(pk=2)
            )

        #Creating Payment object with paid=True, associated with order1

        Payment.objects.create(
            order=Order.objects.get(pk=1),
            intent_id='intent_id',
            amount=3.00,
            created=datetime.datetime(year=2020, month=7, day=15),
            confirmedAt=datetime.datetime(year=2020, month=7, day=15),
            paid=True,
        )

        #Creating Payment object with paid=False, associated with order2

        Payment.objects.create(
            order=Order.objects.get(pk=2),
            intent_id='intent_id',
            amount=2,
            created=datetime.datetime(year=2020, month=7, day=15),
            paid=False,
        )
        

    # TESTS

    # Test if get_orders returns queryset containing only Order instances
    # which created >= start_date and created <= end_date
    # or none when no one exists
    # params: start_date -> datetime, end_date -> datetime

    def test_get_orders_gets_correct_data(self):
        start_date=datetime.datetime(year=2020, month=7, day=1)
        end_date=datetime.datetime(year=2020, month=7, day=31)
        
        qs = raport.Raport.get_orders(start_date, end_date)

        for obj in qs:
            self.assertTrue(obj.created >= utc.localize(start_date))
            self.assertTrue(obj.created <= utc.localize(end_date))
            self.assertIsInstance(obj, Order)


        wrong_start_date=datetime.datetime(year=2010, month=7, day=1)
        wrong_end_date=datetime.datetime(year=2010, month=7, day=31)

        empty_qs = raport.Raport.get_orders(wrong_start_date, wrong_end_date)

        self.assertEqual(empty_qs, None)
        

    # Test if get_paid_orders returns queryset containing only Order instances
    # associated with Payment instances among which at least one has attr paid=True
    # or None if None value given
    # params: orders -> list of Order object

    def test_get_paid_orders_gets_correct_data(self):
        orders = Order.objects.all()
        paid_orders = raport.Raport.get_paid_orders(orders)

        if orders:
            for order in paid_orders:
                payments = Payment.objects.filter(order=order)
                paid = False

                for payment in payments:
                    if payment.paid:
                        paid = True

                self.assertEqual(payment.paid, True)
        else:
            self.assertEqual(paid_orders, None)


    # Test if get_sold_giftcards return list of GiftCard instances 
    # or empty list if paid_orders==None
    # params: 
    #   paid_orders -> Queryset of Order instances
    #   brand -> Brand instance

    def test_get_sold_giftcards_gets_correct_data(self):
        brand = Brand.objects.get(pk=1)
        paid_orders = Order.objects.all()

        giftcards = raport.Raport.get_sold_giftcards(paid_orders, brand)

        self.assertIsInstance(giftcards, list)

        for obj in giftcards:
            self.assertIsInstance(obj, GiftCard)

    # Test if get_total_value returns correct decimal value
    # or 0 if given empty list
    # params: sold_giftcards -> list of GiftCard instances

    def test_get_total_value_return_correct_data(self):
        sold_giftcards = GiftCard.objects.filter(order=Order.objects.get(pk=1))
        empty_list = []
        total_value = raport.Raport.get_total_value(sold_giftcards)
        total_value_for_empty_list = raport.Raport.get_total_value(empty_list)

        self.assertEqual(total_value, decimal.Decimal(3.00))
        self.assertEqual(total_value_for_empty_list, 0)

    # Test if get_total_price returns correct decimal value
    # or 0 if given empty list
    # params: sold_giftcards -> list of GiftCard instances

    def test_get_total_price_returns_correct_data(self):
        sold_giftcards = GiftCard.objects.filter(order=Order.objects.get(pk=1))
        empty_list = []
        total_price = raport.Raport.get_total_price(sold_giftcards)
        total_price_for_empty_list = raport.Raport.get_total_price(empty_list)

        self.assertEqual(total_price, decimal.Decimal(3.00))
        self.assertEqual(total_price_for_empty_list, 0)


    # Test if get_sold_giftcards_number returns correct int value
    # or 0 if given empty list
    # params: params: sold_giftcards -> list of GiftCard instances

    def test_get_sold_giftcards_number_returns_correct_data(self):
        sold_giftcards = GiftCard.objects.filter(order=Order.objects.get(pk=1))
        empty_list = []

        sold_giftcards_number = raport.Raport.get_sold_giftcards_number(sold_giftcards)
        sgn_for_empty_list = raport.Raport.get_sold_giftcards_number(empty_list)

        self.assertEqual(sold_giftcards_number, 3)
        self.assertEqual(sgn_for_empty_list, 0)


    # Test if get_income return correct rounded decimal value 
    # params: 
    #   total_price -> decimal value
    #   COMMISSION -> mocked settings attribute (float)

    def test_get_income_returns_correct_data(self):
        total_price = decimal.Decimal(3.0)

        with self.settings(COMMISSION = 0.1):
            self.assertEqual(raport.Raport.get_income(total_price), round(decimal.Decimal(0.3), 2))

    # Test if generate_raport_data returns correct Raport object 
    # with correct attributes values

    def test_generate_raport_data_returns_correct_data(self):
        start_date=datetime.datetime(year=2020, month=7, day=1)
        end_date=datetime.datetime(year=2020, month=7, day=31)
        brand = Brand.objects.get(pk=1)

        raport_obj = raport.Raport.generate_raport_data(start_date, end_date, brand)

        self.assertIsInstance(raport_obj, raport.Raport)
        
        self.assertEqual(raport_obj.brand, brand)
        self.assertEqual(raport_obj.start_date, start_date)
        self.assertEqual(raport_obj.end_date, end_date)
        self.assertEqual(raport_obj.total_price, decimal.Decimal(3.00))
        self.assertEqual(raport_obj.total_value, decimal.Decimal(3.00))
        self.assertEqual(raport_obj.sold_giftcards_number, 3)
        self.assertEqual(raport_obj.income, round(decimal.Decimal(0.15), 2))

    
    
        
