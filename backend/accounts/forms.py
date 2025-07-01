from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


# this takes username and email
class RegistrationForm(UserCreationForm):
    phone = forms.CharField(
        required=True,
        widget=forms.NumberInput(attrs={
            'type': 'tel',
            'id': 'phone'
        })
    )
    email = forms.EmailField(label='آدرس ایمیل',
        required=False,
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'id': 'email',
        })
    )

    password1 = forms.CharField(label='رمزعبور',
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'id': 'password',
        })
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
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