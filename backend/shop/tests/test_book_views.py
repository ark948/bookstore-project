import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from accounts.tests.conftest import user, custom_user, custom_employee
from shop.models import Book
from shop.forms import (
    NewBookForm
)


@pytest.mark.django_db
def test_books_list_inaccessible(client, custom_user):
    client.force_login(custom_user)
    response = client.get(reverse('shop:books-list'))

    assert response.status_code == 403


@pytest.mark.django_db
def test_books_list(client, custom_employee, book):
    client.login(username='user1@email.com', password='test123*A')
    response = client.get(reverse("shop:books-list"))

    assert response.status_code == 200
    assertTemplateUsed(response, 'shop/books/books-list.html')
    assert response.context['books'][0] == book



@pytest.mark.django_db
def test_books_add_book(client, custom_employee, author, publication, language, genre):
    client.force_login(custom_employee)
    
    form_data = {
        'title': 'A new book',
        'authors': [author.pk],
        'publisher': publication.pk,
        'language': language.pk,
        'original_language': language.pk,
        'page_count': 200,
        'genres': [genre.pk,],
    }

    url = reverse('shop:add-book')
    response = client.post(url, form_data)
    assert response.status_code == 200

    book = Book.objects.filter(title='A new book').first()
    assert book is not None
