from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.

from .forms import (
    RegistrationForm,
    CustomUserCreationForm
)

# signup
# login
# logout
# account recovery
# profile

def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('home:index'))
    form = RegistrationForm()
    return render(request, 'accounts/signup.html', {"form": form})

def login():
    pass

def logout():
    pass