from django import forms
from .models import GiftCard
from django.conf import settings
from decimal import Decimal

class GiftCardAdminCreateForm(forms.ModelForm):
    quantity = forms.IntegerField(initial=1)

    class Meta:
        model = GiftCard
        fields = ['value', 'price', 'brand']


