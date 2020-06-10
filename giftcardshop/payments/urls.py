from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<order_id>/', views.CheckoutView.as_view(), name='checkout'),
    path('processed/<intent_id>/', views.post_payment_view, name='payment_processed'),
]