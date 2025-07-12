from django import forms

# Create your forms here

from .models import Book

class NewBookForm(forms.ModelForm):
    title = forms.CharField(label="عنوان", max_length=256, required=True)
    class Meta:
        model = Book
        fields = ('title', )