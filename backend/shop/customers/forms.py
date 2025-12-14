from django import forms

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
