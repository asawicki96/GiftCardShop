from django.shortcuts import render
from django.views import View
from braces.views import LoginRequiredMixin
from orders.models import Order, OrderItem
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from .models import Payment
import stripe
import datetime
from giftcards.models import GiftCard
from django.core.mail import send_mail


stripe.api_key = 'sk_test_XE7g6ioM7V5xWwhhKa5SbJCD00NzqYPUZD'

# Create your views here.


class CheckoutView(View, LoginRequiredMixin):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        price = int(order.get_total_cost())*100

        intent = stripe.PaymentIntent.create(
                amount = price,
                currency = 'pln',
                metadata={
                    'integration_check': 'accept_a_payment',
                },
            )
        
        payment = Payment(
            order = order,
            intent_id = intent.id,
            amount = order.get_total_cost()
        )
        payment.save()

        return render(request, 'payments/checkout.html', {'client_secret': intent.client_secret, 'intent_id': intent.id})

def post_payment_view(request, intent_id):
    payment = get_object_or_404(Payment, intent_id=intent_id)
    payment.paid = True
    payment.confirmedAt = datetime.datetime.now()
    payment.save()
    order = payment.order
    send_codes(order)

    return render(request, "payments/success.html")

def send_codes(order):
    items = OrderItem.objects.filter(order=order)

    giftcards = []
    for item in items:
        giftcard = get_object_or_404(GiftCard, pk=item.id)
        giftcards.append(giftcard)

    subject = "GiftCardShop order: " + str(order.id) + " payment received."
    from_email = settings.WEBSITE_EMAIL
    recipient_list = [order.email]

    message = '''We have received your payment, thank You for shopping in our store.
                Your giftcards codes:
                '''
    for giftcard in giftcards:
        message += (str(giftcard) + ' ' + 'Code:' + str(giftcard.uuid) + '\n')

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
         
      