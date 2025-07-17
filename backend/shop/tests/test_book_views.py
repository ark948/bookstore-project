import pytest
from django.test import TestCase
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_books_list(client, book):
    response = client.get(reverse("shop:books-list"))
    assertTemplateUsed(response, "shop/books/books-list.html")