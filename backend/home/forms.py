from django.forms.models import ModelForm
from django import forms

from home.models import PublicMessage

class PublicMessageForm(ModelForm):
    body = forms.CharField(
        widget=forms.Textarea()
    )
    class Meta:
        model = PublicMessage
        fields = ("name", "email", "phone", "subject", "body")