from celery import task
from django.conf import settings
from django.core.mail import send_mail
from giftcards.models import GiftCard
from .models import Order
from payments.models import Payment
from django.shortcuts import get_object_or_404
import datetime

@task
def send_codes(order_id):
    order = get_object_or_404(Order, pk=order_id)
    giftcards = GiftCard.objects.filter(order=order)
    
    subject = "GiftCardShop order: " + order_id + " payment received."
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

@task
def send_confirmation_mail(order_id):
    order = get_object_or_404(Order, pk=order_id)
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

@task
def make_unpaid_orders_outdated():
    #WIP
    #TO DO: filter unpaid orders older than timedelta and set outdated True
    timedelta = datetime.timedelta(days=3)
    min_creation_date = datetime.datetime.now() - timedelta
    
    orders = Order.objects.filter(created__lte=min_creation_date).filter(outdated=False)

    if not orders:
        return None

    for order in orders:
        payment = Payment.objects.filter(order=order).filter(paid=True)
        
        if not payment:
            order.outdated = True
            order.save()
            restore_giftcard(order)
  
def restore_giftcard(order):
    giftcards = GiftCard.objects.filter(order=order)
    if not giftcards:
        raise Exception("No gifctards related to order:{} found".format(order.id))
    
    for giftcard in giftcards:
        g_card = get_object_or_404(GiftCard, pk=giftcard.id)
        g_card.order = None
        g_card.save()