import django_filters
from shop.models import (
    Book, Genre, Language
)

class BookFilter(django_filters.FilterSet):
    genres = django_filters.ModelChoiceFilter(
        queryset=Genre.objects.all(),
        empty_label="Any",
        label="ژانر"
    )

    language = django_filters.ModelChoiceFilter(
        queryset=Language.objects.all(),
        empty_label="همه",
        label="زبان"
    )

    class Meta:
        model = Book
        fields = (
            "genres",
            "language",
        )