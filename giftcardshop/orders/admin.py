from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class OrderItemInline(admin.StackedInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 
        'last_name', 
        'address', 
        'postal_code', 
        'city', 
        'created',
        'get_total_cost',
        'paid']

    inlines = [OrderItemInline]