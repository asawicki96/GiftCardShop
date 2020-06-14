from django.contrib import admin
from .models import GiftCard
from .forms import GiftCardAdminCreateForm
from taggit.managers import TaggableManager

# Register your models here.

@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display = [
        'brand_name', 
        'get_categories',
        'price', 
        'value', 
        'created']

    list_filter = ['created', 'brand__name', 'brand__category']
    search_fields = ['brand__name', 'brand__category']        

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            return GiftCardAdminCreateForm
        return super().get_form(request, obj, **kwargs)
    
    def brand_name(self, obj):
        return obj.brand.name

