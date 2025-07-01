from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.

from .forms import (
    CustomUserSignUpForm
)

# signup
# login
# logout
# account recovery
# profile

def signup(request):
    form = CustomUserSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login():
    pass

def logout():
    pass