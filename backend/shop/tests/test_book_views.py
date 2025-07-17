import pytest
from django.test import TestCase
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from accounts.tests.conftest import user

@pytest.mark.skip
@pytest.mark.django_db
def test_books_list(client, user, book):
    response = client.get(reverse("shop:books-list"))
    assert response.status_code == 403