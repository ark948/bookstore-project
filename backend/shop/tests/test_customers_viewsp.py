import pytest
import logging

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_customers_index_page(client):
    response = client.get(reverse("shop:customers_index"))

    assert response.status_code == 200
    assertTemplateUsed(response, "shop/customers/index.html")