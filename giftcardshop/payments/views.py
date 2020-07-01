from django.shortcuts import render, redirect
from django.views import View
from braces.views import LoginRequiredMixin
from orders.models import Order
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from .models import Payment
import stripe
import datetime
from giftcards.models import GiftCard
from django.core.mail import send_mail
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = 'sk_test_XE7g6ioM7V5xWwhhKa5SbJCD00NzqYPUZD'

# Create your views here.


class CheckoutView(LoginRequiredMixin, View):
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


@csrf_exempt
def post_payment_view(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
      json.loads(payload), stripe.api_key
    )
    except ValueError as e:
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        intent_id = payment_intent.id
        payment = get_object_or_404(Payment, intent_id=intent_id)
        payment.paid = True
        payment.confirmedAt = datetime.datetime.now()
        payment.save()

        order = payment.order
        send_codes(order)

        return HttpResponse(status=200)

    else:
      # Unexpected event type
        return HttpResponse(status=400)

def payment_success(request):
    if request.method == 'GET':
        return render(request, "payments/success.html")

def send_codes(order):
    giftcards = GiftCard.objects.filter(order=order)

    subject = "GiftCardShop order: " + str(order.id) + " payment received."
    from_email = settings.WEBSITE_EMAIL
    recipient_list = [order.user.email]

    message = "We have received your payment, thank You for shopping in our store. \nYour giftcards codes:\n"
            

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
   
      