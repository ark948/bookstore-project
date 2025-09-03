from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib import messages

from accounts.decorators import role_required

# Create your views here.

from accounts.models import UserProfile

from .forms import (
    CustomUserSignUpForm,
    EmailLoginForm,
    CustomerAddressForm,
    CustomerAddressForm2
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
            if user != None:
                login(request, user)
                return render(request, 'accounts/messages/login_success.html')
            messages.error(request, "نام کاربری و یا رمز عبور اشتباه است.")
            return redirect(reverse("accounts:login"))
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


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/profile.html")


@role_required('user')
def add_address(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CustomerAddressForm(request.POST)
        if form.is_valid():
            user_profile = request.user.profile
            user_profile.address = form.cleaned_data['address']
            user_profile.save()
            messages.success(request, "آدرس با موفقیت ثبت شد.")
            return redirect(reverse("accounts:profile"))
        else:
            messages.error(request, "خططای رخ داده است. لطفا دوباره امتحان کنید.")
            return render(request, "accounts/add_address.html", {'form': form})
    form = CustomerAddressForm()
    return render(request, "accounts/add_address.html", {'form': form})


@role_required('user')
def add_address_v2(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CustomerAddressForm2(request.POST)
        if form.is_valid():
            user_profile = request.user.profile
            user_profile.address = form.cleaned_data['address']
            user_profile.save()
            messages.success(request, "آدرس با موفقیت ثبت شد.")
            return redirect(reverse("accounts:profile"))
        else:
            messages.error(request, "خططای رخ داده است. لطفا دوباره امتحان کنید.")
            return render(request, "accounts/add_address_2.html", {'form': form})
    form = CustomerAddressForm2()
    return render(request, "accounts/add_address_2.html", {'form': form})


def load_city_names(request: HttpRequest) -> JsonResponse:
    pass