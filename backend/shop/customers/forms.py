from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

ITEM_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class AddCommentForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 8,
            'cols': 40
        })
    )

    has_purchased = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class ItemAddForm(forms.Form):
    quantity = forms.IntegerField(
        label='تعداد',
        widget=forms.NumberInput(
            attrs={
                'min': 1,
                'max': 10,
                'value': 1,
            }
        )
    )

    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'quantity',
            'override',
            Submit('submit', 'بروزرسانی', css_class='btn-accent btn-xs')
        )