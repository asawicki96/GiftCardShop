from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from giftcards.models import GiftCard
from django.views import View
from braces.views import LoginRequiredMixin

# Create your views here.

class CartAddView(View):
    def post(self, request):
        cart = Cart(request)
        giftcard_id = request.POST.get('giftcard_id', None)

        giftcard = get_object_or_404(GiftCard, id=giftcard_id)
        cart.add(request, giftcard=giftcard)

        return redirect('cart_detail')

class CartRemoveView(View):
    def get(self, request, giftcard_id):
        cart = Cart(request)
        giftcard = get_object_or_404(GiftCard, id=giftcard_id)
        cart.remove(request, giftcard)

        return redirect('cart_detail')

class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        if cart.get_len() == 0:
            cart = None

        context = {
            'cart': cart
        }

        return render(request, 'cart/detail.html', context)
        
