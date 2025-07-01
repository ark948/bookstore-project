from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser


class CustomUserSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'id': 'email'
        })
    )

    class Meta:
        model = CustomUser
        fields = (
            "email",
        )


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'id': 'email'
        })
    )

    class Meta:
        model = CustomUser
        fields = ("email",)


class EmailLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}), required=True)
    password = forms.CharField(
        label="رمزعبور",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password"
        }),
    )