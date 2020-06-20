from django.db import models
from orders.models import Order

# Create your models here.

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    intent_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add= True)
    paid = models.BooleanField(default=False)
    confirmedAt = models.DateTimeField(null=True)

