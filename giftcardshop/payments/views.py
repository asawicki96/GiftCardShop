from django.shortcuts import render
from django.views import View
from braces.views import LoginRequiredMixin
from orders.models import Order
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
import stripe

# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.max_network_retries = 2

class CheckoutView(View, LoginRequiredMixin):
    def get(self, request, order_id):
        return render(request, 'payments/checkout.html', {'order_id': order_id})

    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        price = int(order.get_total_cost())*100

        intent = stripe.PaymentIntent.create(
            amount = price,
            currency = 'PLN',
            metadata={
                'integration_check': 'accept_a_payment',
            },
        )

        keys = {
            'publishableKey': settings.STRIPE_PUBLISHABLE_KEY,
            'clientSecret': intent.client_secret
        }

        try:
            return JsonResponse(keys)
        except Exception as e:
            return JsonResponse(error=str(e))

        
