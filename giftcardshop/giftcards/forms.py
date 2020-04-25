from django import forms
from .models import GiftCard

class GiftCardAdminCreateForm(forms.ModelForm):
    quantity = forms.IntegerField(initial=1)

    class Meta:
        model = GiftCard
        fields = '__all__'

        

