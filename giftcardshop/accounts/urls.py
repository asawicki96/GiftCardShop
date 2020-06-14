from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.AccountRegisterView.as_view(), name='register'),
    path('edit/', views.AccountEditView.as_view(), name='edit'),
    path('overview/', views.ProfileOverwievView.as_view(), name='overview'),

]
