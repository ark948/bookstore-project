from django import forms

# Create your forms here

from .models import Book

class NewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"