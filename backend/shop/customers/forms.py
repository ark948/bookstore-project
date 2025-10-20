from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

ITEM_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class AddCommentForm(forms.Form):
    title = forms.CharField(max_length=60, required=False)
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'comment_body_id',
            'class': "textarea textarea-success",
            'rows': 8,
            'cols': 40
        })
    )
    anonymous = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
            'class': "checkbox checkbox-md checkbox-accent"
        }
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'input input-success',
        })


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