from django.forms.models import ModelForm

from home.models import PublicMessage

class PublicMessageForm(ModelForm):
    class Meta:
        model = PublicMessage
        fields = "__all__"