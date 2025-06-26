from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


# this takes username and email
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


# this only takes email
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')