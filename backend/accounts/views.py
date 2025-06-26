from django.shortcuts import render

# Create your views here.

from .forms import (
    RegistrationForm,
    CustomUserCreationForm
)

# signup
# login
# logout

def signup(request):
    form = RegistrationForm()
    return render(request, 'accounts/signup.html', {"form": form})

def login():
    pass

def logout():
    pass