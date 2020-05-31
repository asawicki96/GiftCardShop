from django.urls import path
from . import views

urlpatterns = [
    path('list/<slug>/<ordering>/', views.GiftCardsLisView.as_view(), name='giftcards_list'),
]
