from django.contrib import admin
from .models import Order
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'created',
        'get_total_cost',
        ]
