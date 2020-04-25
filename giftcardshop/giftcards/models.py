from django.db import models
from brands.models import Brand
from taggit.managers import TaggableManager
import uuid

# Create your models here.

class GiftCard(models.Model):
    brand = models.ForeignKey(to=Brand, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=256, blank=True, null=True)
    category = models.CharField(max_length=256, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    code = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "Gift card: " + self.brand.name + " amount: " + str(self.amount)

        



