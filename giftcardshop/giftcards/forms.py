from django import forms
from .models import GiftCard

class GiftCardAdminCreateForm(forms.ModelForm):
    quantity = forms.IntegerField(initial=1)

    class Meta:
        model = GiftCard
        fields = '__all__'

    def save(self, commit=True):
        cleanedData = self.cleaned_data
        quantity = cleanedData.get('quantity', None)
        categories = cleanedData.get('category', None)

        for i in range(quantity):
            g_card = GiftCard.objects.create(
                brand = cleanedData.get('brand', None),
                purchase_amount = cleanedData.get('purchase_amount', None),
                price = cleanedData.get('price', None),
                description = cleanedData.get('description', None)
            )
            for category in categories:
                g_card.category.add(category)

            g_card = super().save(commit=commit)
            
        return g_card
        

