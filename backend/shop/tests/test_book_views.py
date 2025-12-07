import pytest
import logging
from pytest_lazy_fixtures import lf
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from accounts.tests.conftest import user, custom_employee, custom_admin, custom_manager
from shop.models import Book
from shop.books.forms import (
    BookForm
)

# Capturing logs inside test functions does not work
# Only kept as reference

@pytest.mark.django_db
def test_books_list_inaccessible(client, user, caplog):
    with caplog.at_level(logging.ERROR, logger='django.request'):
        client.force_login(user)
        response = client.get(reverse('shop:books_list'))
        assert response.status_code == 403


@pytest.mark.django_db
def test_books_list(client, custom_employee, book_obj):
    client.force_login(custom_employee)
    response = client.get(reverse('shop:books_list'))

    assert response.status_code == 200
    assertTemplateUsed(response, 'shop/books/books-list.html')
    assert response.context['page_obj'][0] == book_obj['book']


@pytest.mark.django_db
@pytest.mark.parametrize("user_fixtures, expected_status", [
    (lf("user"), 403),
    (lf("custom_manager"), 403),
    (lf("custom_admin"), 403),
    (lf("custom_employee"), 200),
])
def test_books_list_only_accessible_to_employee(client, user_fixtures, expected_status):
    client.force_login(user_fixtures)
    response = client.get(reverse('shop:books_list'))
    assert response.status_code == expected_status


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
        'pub_date': '2020',
        'format': 'paperback',
        'price': 200,
        'age_recommendation': 'Unavailable',
    }

    url = reverse('shop:add_book')
    response = client.post(url, form_data)
    assert response.status_code == 302
    assert response.url == reverse('shop:books_list')

    book = Book.objects.filter(title='A new book').first()
    assert book is not None
    assert isinstance(book, Book)
    assert book.title == "A new book"
    assert list(book.authors.all()) == [book_obj['author']]


@pytest.mark.django_db
def test_book_details(client, custom_employee, book_obj):
    client.force_login(custom_employee)

    response = client.get(reverse("shop:book_details", kwargs={'pk': book_obj['book'].id}))
    assert response.context['item'] == book_obj['book']