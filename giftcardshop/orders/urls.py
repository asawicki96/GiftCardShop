from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.OrderCreate.as_view(), name='order_create'),
    path('detail/<order_id>/', views.OrderDetailView.as_view(), name='detail'),
]
