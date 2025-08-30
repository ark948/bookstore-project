from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser

class CustomerAddressForm(forms.Form):
    post_code = forms.CharField(label="کد پستی", min_length=5, required=True)
    province = forms.ChoiceField(label='استان', required=True)
    city = forms.ChoiceField(label='شهر', required=True)
    landline = forms.CharField(label='', widget=forms.IntegerField(), required=False)
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': "textarea textarea-success",
            'rows': 8,
            'cols': 40
        }),
        required=True
    )

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