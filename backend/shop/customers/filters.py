import django_filters

from shop.models import (
    Book, Genre, Author, Publication, Language, Tag
)

class BooksFilter(django_filters.FilterSet):
    authors = django_filters.ModelMultipleChoiceFilter(
        queryset=Author.objects.all(),
        label="نویسنده",
    )

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

    original_language = django_filters.ModelChoiceFilter(
        queryset=Language.objects.all(),
        empty_label="همه",
        label="زبان اصلی"
    )

    edition = django_filters.NumberFilter(
        lookup_expr='exact'
    )

    page_count = django_filters.RangeFilter()

    genres = django_filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(),
        label="ژانر"
    )

    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        label="برچسب"
    )

    class Meta:
        model = Book
        fields = (
            "authors",
            "publisher",
            "language",
            "original_language",
            "edition",
            "page_count",
            "genres",
            "tags",
        )