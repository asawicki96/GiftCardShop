from django.shortcuts import render, redirect
from django.views import View
from braces.views import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .models import GiftCard
from brands.models import Brand
from cart.cart import Cart

class GiftCardsLisView(View, LoginRequiredMixin):
    def get(self, request, slug=None, ordering=None):
        cart = Cart(request)
    
        page = request.GET.get('page', None)

        if ordering == 'value':
            ordering = '-value'
        else:
            ordering = 'value'
        
        brand = get_object_or_404(Brand, slug=slug)
        giftcards = GiftCard.objects.filter(brand=brand, order__isnull=True).exclude(id__in=cart.cart.keys())

        categories = brand.category.all()

        similar_brands = Brand.objects.filter(category__in=categories).distinct().exclude(slug=brand.slug)[:15]

        giftcards = giftcards.order_by(ordering)
        
        paginator = Paginator(giftcards, 12)
        page_obj = paginator.get_page(page)

        context = {
            'brand': brand,
            'page_obj': page_obj,
            'similar_brands': similar_brands
        }

        return render(request, 'giftcards/list.html', context)
