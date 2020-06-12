from django.contrib import admin
from .models import Payment

# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'intent_id', 'amount', 'created', 'confirmedAt', 'paid'] 
    list_filter = ['created', 'paid']
    search_fields = ['intent_id', 'order']