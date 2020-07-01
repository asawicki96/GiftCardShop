from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<order_id>/', views.CheckoutView.as_view(), name='checkout'),
    path('webhook/', views.post_payment_view, name='post_payment'),
    path('success/', views.payment_success, name='payment_success'),
]