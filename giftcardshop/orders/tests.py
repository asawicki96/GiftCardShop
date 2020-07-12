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
from django.http import HttpResponse

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

        Order.objects.create(
            user=User.objects.get(pk=1), 
            created=datetime.datetime(year=2020, month=7, day=15))
        Order.objects.create(
            user=User.objects.get(pk=1), 
            created=datetime.datetime(year=2020, month=7, day=15))
        Order.objects.create(
            user=User.objects.get(pk=1), 
            created=datetime.datetime(year=2020, month=6, day=15))

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

        
        '''Creating 6 GiftCard objects;
           3 associated with brand1 & order1
           3 associated with brand2 & order2'''

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

    def test_generate_raport_data_returns_correct_data(self):
        ''' Test if generate_raport_data returns correct Raport object 
            with correct attributes values
            params:
                start_date -- datetime.date
                end_date -- datetime.date
                brand -- Brand'''
            
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

    
    # Raport Factory tests

class RaportFactoryTestCase(TestCase):
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

        Order.objects.create(
            user=User.objects.get(pk=1), 
            created=datetime.datetime(year=2020, month=7, day=15))
        Order.objects.create(
            user=User.objects.get(pk=1), 
            created=datetime.datetime(year=2020, month=7, day=15))
        Order.objects.create(
            user=User.objects.get(pk=1), 
            created=datetime.datetime(year=2020, month=6, day=15))

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

        
        ''' Creating 6 GiftCard objects;
            3 associated with brand1 & order1
            3 associated with brand2 & order2'''

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
            created=datetime.date(year=2020, month=7, day=15),
            confirmedAt=datetime.date(year=2020, month=7, day=15),
            paid=True,
        )

        #Creating Payment object with paid=True, associated with order2

        Payment.objects.create(
            order=Order.objects.get(pk=2),
            intent_id='intent_id',
            amount=3.00,
            created=datetime.date(year=2020, month=7, day=15),
            paid=True,
        )

    # TESTS

    def test_get_raport_set_returns_correct_data(self):
        ''' Test if RaportFactory returns correct RaportSet object 
            when list of Brand objects given
            params:
            start_date -- datetime.date
            end_date -- datetime.date
            brands -- list of Brand objects'''

        start_date = datetime.date(year=2020, month=7, day=1)
        end_date = datetime.date(year=2020, month=7, day=31)
        brands = [Brand.objects.get(pk=1), Brand.objects.get(pk=2)]
        empty_brands_list = []

        raport_set = raport.RaportFactory.get_raport_set(
            start_date=start_date, 
            end_date=end_date, 
            brands=brands)
        raport_set_not_brands = raport.RaportFactory.get_raport_set(
            start_date=start_date, 
            end_date=end_date, 
            brands=empty_brands_list)

        self.assertIsInstance(raport_set, raport.RaportSet)
        self.assertIsInstance(raport_set.raports, list)
        self.assertEqual(raport_set.total_price, round(decimal.Decimal(6.00), 2))
        self.assertEqual(raport_set.total_value, round(decimal.Decimal(6.00), 2))
        self.assertEqual(raport_set.total_income, round(decimal.Decimal(0.3), 2))
        self.assertEqual(raport_set.sold_giftcards_number, 6)
        
        for obj in raport_set.raports:
            self.assertIsInstance(obj, raport.Raport)

        # In case of empty brands list given
        self.assertEqual(raport_set_not_brands.raports, None)
       
        # In case of no orders in given timeframes
        start_date = datetime.date(year=2010, month=7, day=1)
        end_date = datetime.date(year=2010, month=7, day=31)

        raport_set = raport.RaportFactory.get_raport_set(
            start_date=start_date, 
            end_date=end_date, 
            brands=brands)
        
        self.assertIsInstance(raport_set, raport.RaportSet)
        self.assertIsInstance(raport_set.raports, list)
        self.assertEqual(raport_set.total_price, 0)
        self.assertEqual(raport_set.total_value, 0)
        self.assertEqual(raport_set.total_income, 0)
        self.assertEqual(raport_set.sold_giftcards_number, 0)
        

    def test_export_returns_correct_data(self):
        ''' Test if function returns HttpResponse object or
            raises Exception when None or not RaportSet object given'''

        start_date = datetime.date(year=2020, month=7, day=1)
        end_date = datetime.date(year=2020, month=7, day=31)
        brands = [Brand.objects.get(pk=1), Brand.objects.get(pk=2)]
        empty_brands_list = []

        raport_set = raport.RaportFactory.get_raport_set(
            start_date=start_date, 
            end_date=end_date, 
            brands=brands)

        response = raport.RaportCsvExporter.export(raport_set)
        
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response['Content-Disposition'], \
            'attachment; filename="Raport:from_date-2020-07-01_to_date-2020-07-31"')

        # Not RaportSet object given
        self.assertRaises(Exception, raport.RaportCsvExporter.export, 1)
        self.assertRaises(Exception, raport.RaportCsvExporter.export, None)