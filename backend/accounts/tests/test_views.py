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
    assertTemplateUsed(response, "accounts/forms/signup.html")


# this is just to check if factory fixture was created successfully
@pytest.mark.django_db
def test_user_factory(user):
    print(user.email)


@pytest.mark.django_db
def test_accounts_signup_redirect_if_logged_in(client: Client, user):
    client.force_login(user)

    response = client.get(reverse("accounts:signup"))
    assert response.status_code == 302