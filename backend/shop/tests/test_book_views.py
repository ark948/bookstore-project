import urllib, requests
import pytest
from django.test import TestCase
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from accounts.tests.conftest import user, custom_user, custom_employee


@pytest.mark.django_db
def test_books_list_inaccessible(client, custom_user):
    client.force_login(custom_user)
    response = client.get(reverse('shop:books-list'))

    assert response.status_code == 403


@pytest.mark.django_db
def test_books_list(client, custom_employee):
    client.login(username='user1@email.com', password='test123*A')
    response = client.get(reverse("shop:books-list"))

    assert response.status_code == 200