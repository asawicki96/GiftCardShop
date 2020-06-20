from django.shortcuts import render, redirect, reverse, get_object_or_404
from cart.cart import Cart
from django.views import View
from braces.views import LoginRequiredMixin
from brands.models import Brand
from .models import Order
from giftcards.models import GiftCard
from django.core.mail import send_mail
from django.conf import settings
from payments.models import Payment
from django.contrib.admin.views.decorators import staff_member_required
from .forms import AdminRaportForm
from . import raport
import csv 
from django.http import HttpResponse
from django.http import HttpResponseForbidden
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.max_network_retries = 2

# Create your views here.

class OrderCreate(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        
        order = Order.objects.create(
            user = request.user
        )

        for item in cart:
            giftcard = get_object_or_404(GiftCard, pk=item['giftcard'].id)

            if giftcard.order:
                cart.remove(request, giftcard)
                return render(request, 'order/no_card.html', {'giftcard': giftcard})

            giftcard.order = order
            giftcard.save()
            
        cart.clear(request)
        self.send_mail(order)

        return redirect('detail', order.id)


    def send_mail(self, order):
        subject = "GiftCardShop order: " + str(order.id) + "."
        from_email = settings.WEBSITE_EMAIL
        recipient_list = [order.user.email]
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

class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        giftcards = GiftCard.objects.filter(order=order)
        payments = Payment.objects.filter(order=order)

        paid = False

        for payment in payments:
            if payment.paid:
                paid = True
                break


        context = {
            'order': order,
            'giftcards': giftcards,
            'paid': paid
        }

        return render(request, 'order/detail.html', context)

class OrderDeleteView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        if order.user != request.user:
            return HttpResponseForbidden()

        payments = Payment.objects.filter(order=order)
        paid = False

        for payment in payments:
            if payment.paid:
                paid = True

        if not paid:
            for payment in payments:
                payment.delete()

            order.delete()
        
        return redirect('overview')
 

@staff_member_required
def admin_export_csv_raport(request, start_date=None, end_date=None, brand=None):
    if request.method == 'GET':
        form = AdminRaportForm()
        return render(request, 'admin/raport.html', {'form': form})

    elif request.method == "POST":
        form = AdminRaportForm(request.POST)
        if form.is_valid():
            cleanedData = form.cleaned_data
            start_date = cleanedData['start_date']
            end_date = cleanedData['end_date']
            brands = cleanedData['brands']

        factory = raport.RaportFactory(start_date=start_date, end_date=end_date, brands=brands)
        raport_set = factory.get_raports()

        response = raport.RaportCsvExporter.export(raport_set)

        return response


        
                
            
            

