from django.db import models
from brands.models import Brand
from taggit.managers import TaggableManager
import uuid

# Create your models here.

class GiftCard(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    purchase_amount = models.DecimalField(max_digits=6, decimal_places=2)
    brand = models.ForeignKey(to=Brand, on_delete=models.CASCADE)
    description = models.CharField(max_length=256, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-created',)
        verbose_name_plural = 'Giftcrads'

    def get_categories(self):
        return ", ".join([obj.name for obj in self.brand.category.all()])
    
    get_categories.short_description = 'Categories'

    def __str__(self):
        return "Gift card: " + self.brand.name + " purchase amount: " + str(self.purchase_amount)

        



