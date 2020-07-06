from django.contrib import admin
from .models import Order
from payments.models import Payment
from giftcards.models import GiftCard
import csv
import datetime
from django.contrib.admin.helpers import ActionForm
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.postgres.forms.ranges import DateRangeField, RangeWidget
from django import forms
from django.shortcuts import redirect
# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'created',
        'get_total_cost',
        'outdated'
        ]



