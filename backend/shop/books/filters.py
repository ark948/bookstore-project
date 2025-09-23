import django_filters
import django_filters.widgets
from shop.models import (
    Book, Genre, Language, Publication, Tag
)

class BookFilter(django_filters.FilterSet):
    publisher = django_filters.ModelChoiceFilter(
        queryset=Publication.objects.all(),
        empty_label="Any",
        label="انتشارات"
    )

    language = django_filters.ModelChoiceFilter(
        queryset=Language.objects.all(),
        empty_label="همه",
        label="زبان"
    )

    genres = django_filters.ModelChoiceFilter(
        queryset=Genre.objects.all(),
        empty_label="Any",
        label="ژانر"
    )

    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Book
        fields = (
            "publisher",
            "language",
            "genres",
            "tags",
        )