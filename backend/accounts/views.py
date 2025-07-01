from django.contrib.auth.forms import AuthenticationForm
from django.http.request import HttpRequest
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

def signup(request: HttpRequest):
    if request.method == "POST":
        form = CustomUserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/messages/signup_success.html')
    form = CustomUserSignUpForm()
    return render(request, 'accounts/forms/signup.html', {'form': form})

def login(request: HttpRequest):
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout():
    pass