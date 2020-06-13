from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return 10
        # return sum(item.get_cost() for item in self.items.all())

    get_total_cost.short_description = 'Total'
    
