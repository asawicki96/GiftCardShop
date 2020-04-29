from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.AccountRegisterView.as_view(), name='register'),

]
