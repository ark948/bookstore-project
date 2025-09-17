from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


from dal import autocomplete

# Create your forms here

from shop.models import Book, Author, Publication, Language, Genre

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        labels = {
            "title": "عنوان",
            "authors": "نویسندگان",
            "publisher": "انتشارات",
            "language": "زبان",
            "original_language": "زبان اصلی",
            "edition": "ویرایش",
            "page_count": "تعداد صفحات",
            "pub_date": "تاریخ انتشار",
            "format": "فرمت",
            "series": "مربوط به مجموعه",
            "ISBN": "ISBN",
            "genres": "ژانر ها",
            "tags": "برچسب ها",
            "price": "قیمت",
            "available": "موجودی",
            "copies_available": "تـعداد در انبار",
            "description": "توضیحات",
            "summary": "خلاصه",
            "age_recommendation": "رده سنی پیشنهادی",
            "keywords": "کلمات کلیدی",
            "translators": "مترجمین",
            "illustrators": "تصویرپردازان",
            "rating": "امتیاز",
        }

    # there is another way to modify label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cover_image'].label = "تصویر"
    

# Unused
# kept for reference
class BookForm_v1_unused(forms.ModelForm):
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


# Unused
# kept for reference
class BookForm_v2_unused(forms.ModelForm):
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


# Unused
# kept for reference
class BookForm_v3_unused(forms.ModelForm):
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


# Unused
# kept for reference
class BookForm_v4_unused(forms.ModelForm):
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
        super(BookForm_v4_unused, self).__init__(*args, **kwargs)
        self.fields['id'].disabled = True  # or use widget attrs

    # dummy validation to test form errors, DELTE LATER
    def clean_title(self):
        title = self.cleaned_data['title']
        if title.startswith('x'):
            raise ValidationError('No name starts with x.')
        return title