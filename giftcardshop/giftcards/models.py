from django.db import models
from brands.models import Brand
from orders.models import Order
import uuid

# Create your models here.

class GiftCard(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    brand = models.ForeignKey(to=Brand, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(to=Order, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ('-created',)
        verbose_name_plural = 'Giftcrads'

    def get_categories(self):
        return ", ".join([obj.name for obj in self.brand.category.all()])
    
    get_categories.short_description = 'Categories'

    def __str__(self):
        return "Gift card: " + self.brand.name + " purchase value: " + str(self.value)

        



