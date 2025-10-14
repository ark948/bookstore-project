import pytest
import logging

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from shop.models import (
    Book,
    Comment,
    Favorite
)
from accounts.tests.conftest import user


@pytest.mark.django_db
def test_customers_index_page(client):
    response = client.get(reverse("shop:customers_index"))

    assert response.status_code == 200
    assertTemplateUsed(response, "shop/customers/index.html")


@pytest.mark.django_db
def test_customers_browse_page(client):
    response = client.get(reverse("shop:customers_browse"))

    assert response.status_code == 200
    assertTemplateUsed(response, "shop/customers/browse.html")
    assert "items" in response.context
    assert list(response.context['items']) == []


# customer's comment test
@pytest.mark.django_db
def test_customers_add_comment(client, book_obj, user):
    client.force_login(user)
    total = Comment.objects.all().count()
    assert total == 0
    comment = {
        'body': 'a nice comment.',
        'book_id': book_obj['book'].pk
    }

    url = reverse('shop:add_comment')
    response = client.post(url, data=comment)
    assert response.status_code == 200

    total = Comment.objects.all().count()
    assert total == 1

    comment = Comment.objects.get(pk=1)
    assert comment.body == 'a nice comment.'


@pytest.mark.django_db
def test_customers_add_to_favorite(client, book_obj, user):
    client.force_login(user)
    total = Favorite.objects.all().count()
    assert total == 0
    headers = {'Hx-Request': 'true'}
    data = {
        'book_id': book_obj['book'].pk
    }
    url = reverse('shop:add_favorite')
    response = client.get(url, data=data, headers=headers)
    assert response.status_code == 200
    total = Favorite.objects.all().count()
    assert total == 1

    favorite = Favorite.objects.get(pk=1)
    assert favorite.user_id == user
    assert favorite.book_id == book_obj['book']
