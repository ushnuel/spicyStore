from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .models import Profile
from shopping_cart.models import Order

from . import forms
# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

def my_profile(request):
    my_user_profile = Profile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(owner=my_user_profile, is_ordered=True)
    context = {
        'orders':my_orders
    }

    return render(request, 'accounts/profile.html', context)

def about(request):
    return render(request, 'accounts/about.html')

def contact(request):
    return render(request, 'accounts/contact.html')