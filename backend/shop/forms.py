from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.urls import reverse_lazy

from dal import autocomplete

# Create your forms here

from .models import Book

class NewBookForm(forms.ModelForm):
    title = forms.CharField(label="عنوان", max_length=256, required=True)

    class Meta:
        model = Book
        fields = (
            'title',
            'authors',
        )
        widgets = {
            'authors': autocomplete.ModelSelect2Multiple(url=reverse_lazy('shop:authors-autocomplete'))
        }