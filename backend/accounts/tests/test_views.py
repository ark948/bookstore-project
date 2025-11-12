import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertContains
from pytest_django.asserts import assertRedirects

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



@pytest.mark.django_db
def test_accounts_load_cities(client: Client, province, cities):
    response = client.get(
        path=reverse('accounts:load_cities'),
        query_params={'province': province.pk}
    )

    response_cities = response.context['cities']
    assert len(response_cities) == len(cities)
    for i in response_cities:
        assert i in cities


@pytest.mark.django_db
def test_accounts_edit_user_comment(client: Client, user, comment_obj):
    client.force_login(user)
    headers={'HTTP_HX-Request': 'true'}
    response = client.post(
        path=reverse('accounts:edit_comment', kwargs={'comment_id': comment_obj.pk}),
        data={'body': "A new body."},
        **headers
    )

    assert response.status_code == 200

    response = client.get(path=reverse('accounts:comments_list'), **headers)
    response_comment_obj = response.context['comments'][0]
    assert  response_comment_obj.body == "A new body."
    assert response_comment_obj.status == "Pending"