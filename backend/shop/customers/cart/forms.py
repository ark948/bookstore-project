from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


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