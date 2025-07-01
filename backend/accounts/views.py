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
    return render(request, 'accounts/signup.html', {'form': form})

def login():
    pass

def logout():
    pass