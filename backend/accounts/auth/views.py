from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from accounts.forms import (
    CustomUserSignUpForm,
    EmailLoginForm,
)


def signup(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect(reverse("home:index"))
    if request.method == "POST":
        form = CustomUserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "ثبت نام با موفقیت انجام شد. میتوانید وارد شوید.")
            return render(request, 'accounts/auth/messages/successful_signup.html')
        else:
            print(form.errors.as_text())
            return render(request, 'accounts/auth/forms/signup.html', {'form': form})
    form = CustomUserSignUpForm()
    return render(request, 'accounts/auth/forms/signup.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:
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
                messages.success(request, "خوش آمدید.")
                return redirect(reverse("home:index"))
            messages.error(request, "نام کاربری و یا رمز عبور اشتباه است.")
            return redirect(reverse("accounts:acc_auth_login"))
    form = EmailLoginForm()
    return render(request, 'accounts/auth/forms/login.html', {'form': form})


@require_http_methods(['POST'])
def logout_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_anonymous:
        return redirect(reverse("home:index"))
    logout(request)
    return redirect(reverse("home:index"))