from django.contrib import admin
from .models import GiftCard, Category
from .forms import GiftCardAdminCreateForm
from taggit.managers import TaggableManager

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'active']
    list_filter = ['created']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display = [
        'brand_name', 
        'get_categories', 
        'price', 
        'purchase_amount', 
        'created', 
        'available']

    list_filter = ['created', 'brand__name', 'category']
    search_fields = ['brand__name', 'category']        

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            return GiftCardAdminCreateForm
        return super().get_form(request, obj, **kwargs)
    
    def brand_name(self, obj):
        return obj.brand.name

