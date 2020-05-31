from django.shortcuts import render, redirect
from cart.cart import Cart
from django.views import View
from braces.views import LoginRequiredMixin
from .forms import OrderCreateForm
from .models import Order, OrderItem

# Create your views here.

class OrderCreate(View, LoginRequiredMixin):
    def get(self, request):
        user = request.user
        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }

        form = OrderCreateForm(initial=initial)

        context = {
            'form': form
        }
        return render(request, 'order/create.html', context)

    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()

            for item in cart:
                giftcard = OrderItem.objects.create(
                    order=order,
                    product=item['giftcard'],
                    price=item['price']
                )

                giftcard.available = False
                giftcard.save()

            cart.clear()

        return redirect('/')
