from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views import View
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy

# Create your views here.


class AccountRegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return result

class IndexView(View):
    def get(self, request):
        return render(request, 'base.html')
        