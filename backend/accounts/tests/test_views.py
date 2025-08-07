import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertContains
from pytest_django.asserts import assertRedirects
from django.db.models import QuerySet

from accounts.models import CustomUser

@pytest.mark.django_db
def test_accounts_signup(client: Client):
    response = client.get(reverse("accounts:signup"))
    assert response.status_code == 200
    assertTemplateUsed(response, "accounts/forms/signup.html")


@pytest.mark.django_db
def test_accounts_signup_redirect_if_logged_in(client: Client, user):
    client.force_login(user)
    response = client.get(reverse("accounts:signup"))
    assert response.status_code == 302



@pytest.mark.django_db
def test_accounts_secure_page_is_inaccessible(client: Client):
    response = client.get(reverse('accounts:prtd-page'))
    assert response.status_code == 403


@pytest.mark.django_db
def test_accounts_secure_page_is_accessed_successfully(client: Client, user):
    client.force_login(user)
    response = client.get(reverse('accounts:prtd-page'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'accounts/private.html')
    assertContains(response, 'This is a secure page.')