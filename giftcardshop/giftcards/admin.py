from django.contrib import admin
from .models import GiftCard
from .forms import GiftCardAdminCreateForm
from taggit.managers import TaggableManager

# Register your models here.

@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'category', 'amount', 'created', 'active']
    list_filter = ['created', 'brand__name', 'category']
    search_fields = ['brand__name', 'category']

   
    class Meta:
        ordering = ('-created',)    

    def save_model(self, request, obj, form, change):
        cd = form.cleaned_data
        quantity = form.cleaned_data['quantity']

        if change == False and quantity > 1:
            for i in range(quantity):
                g = GiftCard.objects.create(
                    brand = cd['brand'],
                    amount = cd['amount'],
                    description = cd['description'],
                    category = cd['category'],
                )
            

    def get_form(self, request, obj=None, **kwargs):
        if obj == None:
            return GiftCardAdminCreateForm
        return super().get_form(request, obj, **kwargs)
    
    def brand_name(self, obj):
        return obj.brand.name