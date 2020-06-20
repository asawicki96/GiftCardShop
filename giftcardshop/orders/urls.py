from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.OrderCreate.as_view(), name='order_create'),
    path('detail/<order_id>/', views.OrderDetailView.as_view(), name='detail'),
    path('delete/<order_id>/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('admin/raport/', views.admin_export_csv_raport, name='raport'),
]
