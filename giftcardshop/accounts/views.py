from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views import View
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from braces.views import LoginRequiredMixin
from .forms import UserEditForm
from orders.models import Order
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

class AccountRegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(self.request, user)
            return redirect('index')
        
        return render(request, 'registration/register.html', {'form': form})
    
class AccountEditView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserEditForm(instance=request.user)
        return render(request, 'registration/edit.html', {'form': form})

    def post(self, request):
        form = UserEditForm(instance=request.user, data=request.POST)

        if form.is_valid():
            form.save()
        return redirect('index')

class ProfileOverwievView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)

        context = {
            'orders': orders
        }

        return render(request, 'overview.html', context)