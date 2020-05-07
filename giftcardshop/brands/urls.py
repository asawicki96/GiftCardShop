from django.urls import path
from . import views

urlpatterns = [
    path('list/<category>/', views.BrandListView.as_view(), name='brand_list'),
    path('<slug>/', views.BrandDetailView.as_view(), name='brand_detail'),
]
