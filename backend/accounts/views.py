from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.

from .forms import (
    CustomUserSignUpForm,
    CustomAuthenticationForm
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
    if request.method == "POST":
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print("\nUSER ->", user)
            if user != None:
                login(request, user)
                return render(request, 'accounts/messages/login_success.html')
        else:
            print(f"\n {form.error_messages}")
    form = CustomAuthenticationForm()
    return render(request, 'accounts/forms/login.html', {'form': form})

def logout():
    pass