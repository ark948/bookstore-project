import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from pytest_django.asserts import assertRedirects
from django.db.models import QuerySet



@pytest.mark.django_db
def test_accounts_signup(client: Client):
    response = client.get(reverse("accounts:signup"))

    assert response.status_code == 200
    assertTemplateUsed(response, "accounts/signup.html")


@pytest.mark.django_db
def test_user_factory(user):
    print("SHIT")
    print(user)