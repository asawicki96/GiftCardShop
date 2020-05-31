from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<order_id>', views.CheckoutView.as_view(), name='checkout'),
]