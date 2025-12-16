import pytest
import logging

from django.urls import reverse

from shop.models import (
    Country, Language, Author, Publication, Book, Genre
)


@pytest.mark.django_db
def test_load_book_comments(client, book_obj):
    response = client.get(reverse('shop:load_book_comments', kwargs={book_obj['book'].pk}))
    assert response['items'] == []