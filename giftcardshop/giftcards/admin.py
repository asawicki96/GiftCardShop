from django.contrib import admin
from .models import GiftCard
from .forms import GiftCardAdminCreateForm
from django.conf import settings
from decimal import Decimal

# Register your models here.

@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display = [
        'brand_name', 
        'get_categories',
        'price', 
        'value', 
        'created',
        'updated']

    list_filter = ['created', 'brand__name', 'brand__category']
    search_fields = ['brand__name', 'brand__category']        

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            return GiftCardAdminCreateForm
        return super().get_form(request, obj, **kwargs)
    
    def brand_name(self, obj):
        return obj.brand.name

    def save_model(self, request, obj, form, change):
        cleanedData = form.cleaned_data
        quantity = cleanedData.get('quantity', None)
        
        if quantity:
            brand = cleanedData.get('brand', None)
            value = cleanedData.get('value', None)
            price = cleanedData.get('price', None)

            for i in range(quantity):
                g_card = GiftCard(
                    brand = brand,
                    value = value,
                    price = price
                    )
                g_card.save()
        
        else:
            return super().save_model(request, obj, form, change)

