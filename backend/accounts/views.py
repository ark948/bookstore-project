from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.

from .forms import (
    CustomUserSignUpForm,
    EmailLoginForm
)

from . import utils

# signup
# login
# logout
# account recovery
# profile

def signup(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(reverse("home:index"))
    if request.method == "POST":
        form = CustomUserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/messages/signup_success.html')
    form = CustomUserSignUpForm()
    return render(request, 'accounts/forms/signup.html', {'form': form})

def login(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(reverse("home:index"))
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username = email, password = password)
            print("\n", user)
            if user != None:
                auth_login(request, user)
                return render(request, 'accounts/messages/login_success.html')
    form = EmailLoginForm()
    return render(request, 'accounts/forms/login.html', {'form': form})

def logout():
    pass