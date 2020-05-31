from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.CartAddView.as_view(), name='cart_add'),
    path('remove/<giftcard_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('detail/', views.CartDetailView.as_view(), name='cart_detail'),
]
