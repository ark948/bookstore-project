import pytest
import logging
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from accounts.tests.conftest import user, custom_employee
from shop.models import Book
from shop.forms import (
    NewBookForm
)

# Capturing logs inside test functions does not work
# Only kept as reference
@pytest.mark.django_db
def test_books_list_inaccessible(client, user, caplog):
    with caplog.at_level(logging.WARNING, logger='django.request'):
        client.force_login(user)
        response = client.get(reverse('shop:books-list'))
        assert response.status_code == 403


@pytest.mark.django_db
def test_books_list(client, custom_employee, book_obj):
    client.force_login(custom_employee)
    response = client.get(reverse("shop:books-list"))

    assert response.status_code == 200
    assertTemplateUsed(response, 'shop/books/books-list.html')
    assert response.context['books'][0] == book_obj['book']



@pytest.mark.django_db
def test_books_add_book(client, custom_employee, book_obj):
    client.force_login(custom_employee)
    
    form_data = {
        'title': 'A new book',
        'authors': [book_obj['author'].pk],
        'publisher': book_obj['publication'].pk,
        'language': book_obj['language'].pk,
        'original_language': book_obj['language'].pk,
        'page_count': 200,
        'genres': [book_obj['genre'].pk],
    }

    url = reverse('shop:add-book')
    response = client.post(url, form_data)
    assert response.status_code == 200

    book = Book.objects.filter(title='A new book').first()
    assert book is not None
    assert isinstance(book, Book)
    assert book.title == "A new book"
    assert list(book.authors.all()) == [book_obj['author']]