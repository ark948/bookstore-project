from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


from dal import autocomplete

# Create your forms here

from shop.models import Book, Author, Publication, Language, Genre

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


class QuickBookEditForm(forms.ModelForm):
    id = forms.IntegerField(label="شناسه")
    title = forms.CharField(label="عنوان", max_length=256, required=True)

    class Meta:
        model = Book
        fields = (
            'id',
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
    
    def __init__(self, *args, **kwargs):
        super(QuickBookEditForm, self).__init__(*args, **kwargs)
        self.fields['id'].disabled = True  # or use widget attrs

    # dummy validation to test form errors, DELTE LATER
    def clean_title(self):
        title = self.cleaned_data['title']
        if title.startswith('x'):
            raise ValidationError('No name starts with x.')
        return title


class FullBookEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "full_edit_form"
        self.helper.form_class = "edit_form"
        self.helper.form_method = "post"
        self.helper.add_input(Submit('submit', 'Send'))


class BookFormV2(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'title',
            'authors',
        )

        widgets = {
            'authors': autocomplete.ModelSelect2Multiple(
                url=reverse_lazy('shop:authors-autocomplete')
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['authors'].widget.attrs.update({
            'data-dropdown-parent': "#modal-form-container"
        })


class BookCreationForm(forms.ModelForm):
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