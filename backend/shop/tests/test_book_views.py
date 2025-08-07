import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from accounts.tests.conftest import user, custom_employee
from shop.models import Book
from shop.forms import (
    NewBookForm
)


@pytest.mark.skip
@pytest.mark.django_db
def test_books_list_inaccessible(client, user):
    client.force_login(user)
    response = client.get(reverse('shop:books-list'))

    assert response.status_code == 403


@pytest.mark.skip
@pytest.mark.django_db
def test_books_list(client, custom_employee, book):
    client.force_login(custom_employee)
    response = client.get(reverse("shop:books-list"))

    assert response.status_code == 200
    assertTemplateUsed(response, 'shop/books/books-list.html')
    assert response.context['books'][0] == book


@pytest.mark.skip
@pytest.mark.django_db
def test_books_add_book(client, custom_employee, book_obj):
    client.force_login(custom_employee)
    
    form_data = {
        'title': 'A new book',
        'authors': [book_obj['author']],
        'publisher': book_obj['publication'],
        'language': book_obj['language'],
        'original_language': book_obj['language'],
        'page_count': 200,
        'genres': [book_obj['genre'],],
    }

    url = reverse('shop:add-book')
    response = client.post(url, form_data)
    assert response.status_code == 200

    book = Book.objects.filter(title='A new book').first()
    assert book is not None
