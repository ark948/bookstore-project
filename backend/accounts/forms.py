from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

from .models import CustomUser, Province, City

# THIS IS JUST AN EXAMPLE (how to crispy forms and tailwind together)
class MyForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name', css_class='border border-gray-300 rounded p-2'),
            Field('email', css_class='border border-gray-300 rounded p-2'),
        )
        self.helper.add_input(Submit('submit', 'Submit', css_class='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'))


class CustomerAddressForm_widget_tweaks(forms.Form):
    postal_code = forms.CharField(label="کد پستی", min_length=5, required=True)
    province = forms.ModelChoiceField(label="استان", queryset=Province.objects.all(), empty_label="Select province")
    city = forms.ModelChoiceField(label="شهر", queryset=City.objects.none(), empty_label="Select city")
    landline = forms.CharField(label='تلفن ثابت', widget=forms.NumberInput(), required=False)
    address = forms.CharField(
        label="آدرس",
        widget=forms.Textarea()
    )

    
class CustomerAddressForm_crispy_forms(forms.Form):
    post_code = forms.CharField(label="کد پستی", min_length=5, required=True)
    province = forms.ChoiceField(label='استان', required=True)
    city = forms.ChoiceField(label='شهر', required=True)
    landline = forms.CharField(label='تلفن ثابت', widget=forms.NumberInput(), required=False)
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': "textarea textarea-success",
            'rows': 8,
            'cols': 40
        }),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.field_class = 'mb-4 p-4 rounded border border-gray-300'

class CustomUserSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'id': 'email',
            'placeholder': "johndoe@gmail.com",
            'autocomplete': "off"
        })
    )

    # this is just for demonstration purposes
    # password1 = forms.CharField(
    #     label="Password",
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
    #     help_text=UserCreationForm.password1.help_text,
    # )

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "password1",
            "password2",
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'placeholder': "**********"
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': "**********"
        })



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
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'autocomplete': "off"
        }), 
        required=True
    )
    password = forms.CharField(
        label="رمزعبور",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password"
        }),
    )