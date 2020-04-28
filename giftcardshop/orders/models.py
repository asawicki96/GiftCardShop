from django.db import models
from giftcards.models import GiftCard

# Create your models here.

class Order(models.Model):
    first_name = models.CharField('Name', max_length=50)
    last_name = models.CharField('Surname', max_length=50)
    email = models.EmailField('E-mail')
    address = models.CharField('Address', max_length=250)
    postal_code = models.CharField('Postal code', max_length=20)
    city = models.CharField('City', max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    get_total_cost.short_description = 'Total'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(GiftCard, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
    
