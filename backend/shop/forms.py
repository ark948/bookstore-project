from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.urls import reverse_lazy

from dal import autocomplete

# Create your forms here

from .models import Book, Author, Publication, Language, Genre

class NewBookForm(forms.ModelForm):
    title = forms.CharField(label="عنوان", max_length=256, required=True)
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        label='نویسندگان',
        widget=autocomplete.ModelSelect2Multiple(
            url=reverse_lazy("shop:authors-autocomplete"),
        )
    )
    publisher = forms.ModelChoiceField(
        queryset=Publication.objects.all(),
        label="انتشارات",
        widget=autocomplete.ModelSelect2(
            url=reverse_lazy("shop:publishers-autocomplete"),
        )
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        label="زبان",
        widget=autocomplete.ModelSelect2(
            url=reverse_lazy("shop:languages-autocomplete"),
        )
    )
    original_language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        label="زبان اصلی",
        widget=autocomplete.ModelSelect2(
            url=reverse_lazy("shop:languages-autocomplete"),
        )
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        label="ژانر",
        widget=autocomplete.ModelSelect2Multiple(
            url=reverse_lazy("shop:genres-autocomplete"),
        )
    )

    page_count = forms.IntegerField(label="تعداد صفحات", max_value=9999)

    class Meta:
        model = Book
        fields = (
            'title',
            'authors',
            'publisher',
            'language',
            'original_language',
            'genres',
            'page_count'
        )
        widgets = {
            # 'authors': autocomplete.ModelSelect2Multiple(url=reverse_lazy('shop:authors-autocomplete')),
            # 'publisher': autocomplete.ModelSelect2(url=reverse_lazy('shop:publishers-autocomplete')),
            # 'language': autocomplete.ModelSelect2(url=reverse_lazy('shop:languages-autocomplete')),
            # 'original_language': autocomplete.ModelSelect2(url=reverse_lazy('shop:languages-autocomplete')),
            # 'genres': autocomplete.ModelSelect2Multiple(url=reverse_lazy('shop:genres-autocomplete')),
        }


class EditBookForm(forms.ModelForm):
    pk = forms.CharField(label='شناسه')
    title = forms.CharField(label="عنوان", max_length=256, required=True)

    class Meta:
        model = Book    
        readonly_fields = ('pk', )
        fields = (
            "pk",
            'title',
            'authors',
            'publisher',
            'language',
            'original_language',
            'genres',
            'page_count'
        )
        widgets = {
            'authors': autocomplete.ModelSelect2Multiple(url=reverse_lazy('shop:authors-autocomplete')),
            'publisher': autocomplete.ModelSelect2(url=reverse_lazy('shop:publishers-autocomplete')),
            'language': autocomplete.ModelSelect2(url=reverse_lazy('shop:languages-autocomplete')),
            'original_language': autocomplete.ModelSelect2(url=reverse_lazy('shop:languages-autocomplete')),
            'genres': autocomplete.ModelSelect2Multiple(url=reverse_lazy('shop:genres-autocomplete')),
        }