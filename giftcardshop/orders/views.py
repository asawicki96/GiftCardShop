from django.shortcuts import render, redirect, reverse, get_object_or_404
from cart.cart import Cart
from django.views import View
from braces.views import LoginRequiredMixin
from .forms import OrderCreateForm
from .models import Order, OrderItem
from giftcards.models import GiftCard
from django.core.mail import send_mail
from django.conf import settings
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.max_network_retries = 2

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
                orderItem = OrderItem.objects.create(
                    order=order,
                    product=item['giftcard'],
                    price=item['price']
                )

                giftcard = get_object_or_404(GiftCard, pk=item['giftcard'].id)
                giftcard.available = False
                giftcard.save()
            
            cart.clear()
            self.send_mail(order)

        return redirect('checkout', order.id)


    def send_mail(self, order):
        subject = "GiftCardShop order: " + str(order.id) + "."
        from_email = settings.WEBSITE_EMAIL
        recipient_list = [order.email]
        message = ''' Thank You for Your order. Please submit Your payment to get your giftcard codes.'''
        fail_silently = False
        auth_user = settings.EMAIL_HOST_USER
        auth_password = settings.EMAIL_HOST_PASSWORD
        
        send_mail(
            subject=subject,
            from_email=from_email,
            recipient_list=recipient_list,
            message=message,
            fail_silently=fail_silently,
            auth_user=auth_user,
            auth_password=auth_password
        )

