from django.shortcuts import render, redirect
from django.views import View
from braces.views import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .models import GiftCard
from brands.models import Brand

class GiftCardsLisView(View, LoginRequiredMixin):
    def get(self, request, slug=None, ordering=None):
        page = request.GET.get('page', None)

        if ordering == 'price_descending':
            ordering = '-purchase_amount'
        else:
            ordering = 'purchase_amount'
        
        brand = get_object_or_404(Brand, slug=slug)
        giftcards = GiftCard.objects.filter(brand=brand)

        categories = brand.category.all()

        similar_brands = Brand.objects.filter(category__in=categories).distinct()[:15]

        giftcards = giftcards.order_by(ordering)
        
        paginator = Paginator(giftcards, 12)
        page_obj = paginator.get_page(page)

        context = {
            'brand': brand,
            'page_obj': page_obj,
            'similar_brands': similar_brands
        }

        return render(request, 'giftcards/list.html', context)
