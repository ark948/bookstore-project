import django_filters
from shop.models import (
    Book, Genre
)

class BookFilter(django_filters.FilterSet):
    genres = django_filters.ModelChoiceFilter(
        queryset=Genre.objects.all(),
        empty_label="Any"
    )

    class Meta:
        model = Book
        fields = (
            "genres",
        )