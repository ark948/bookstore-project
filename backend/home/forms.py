from django.forms.models import ModelForm

from home.models import PublicMessage

class PublicMessageForm(ModelForm):
    class Meta:
        model = PublicMessage
        fields = ("name", "email", "phone", "subject", "body")