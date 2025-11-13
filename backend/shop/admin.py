from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

# Register your models here.

from .models import (
    Country,
    Language,
    Translator,
    Illustrator,
    Author,
    Genre,
    Tag,
    Keyword,
    Publication,
    Size,
    Series,
    Book,
    Award,
    Review,
    Discount,
    Comment,
    Order,
    Payment,
)


class BookAuthorsAdminForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=FilteredSelectMultiple(
            verbose_name="Authors",
            is_stacked=False
        )
    )

    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=FilteredSelectMultiple(
            verbose_name="Genres",
            is_stacked=False
        )
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=FilteredSelectMultiple(
            verbose_name="Tags",
            is_stacked=False
        )
    )


class BookAdmin(admin.ModelAdmin):
    form = BookAuthorsAdminForm


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"

class AuthorAdmin(admin.ModelAdmin):
    list_display = ["en_name", "fa_name", "pen_name", "full_name", "books_count"]
    form = AuthorForm


admin.site.register(Country)
admin.site.register(Language)
admin.site.register(Illustrator)
admin.site.register(Translator)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Keyword)
admin.site.register(Publication)
admin.site.register(Size)
admin.site.register(Series)
admin.site.register(Award)
admin.site.register(Review)
admin.site.register(Discount)
admin.site.register(Comment)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Book, BookAdmin)