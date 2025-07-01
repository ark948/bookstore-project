from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseForbidden

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


def login_view(request: HttpRequest):
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
                login(request, user)
                return render(request, 'accounts/messages/login_success.html')
    form = EmailLoginForm()
    return render(request, 'accounts/forms/login.html', {'form': form})


@require_http_methods(['POST'])
def logout_view(request: HttpRequest):
    if request.user.is_anonymous:
        return redirect(reverse("home:index"))
    logout(request)
    return redirect(reverse("home:index"))


# @login_required -> this will redirect user to login page
def protected_view(request: HttpRequest):
    if request.user.is_authenticated == False:
        return HttpResponseForbidden()
    return render(request, 'accounts/private.html')