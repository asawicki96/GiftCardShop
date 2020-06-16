from django import forms
from brands.models import Brand

class DateInput(forms.DateInput):
    input_type = 'date'

class AdminRaportForm(forms.Form):
    start_date = forms.DateField(label="Select start date", widget=DateInput)
    end_date = forms.DateField(label="Select end date", widget=DateInput)
    
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), empty_label=None)