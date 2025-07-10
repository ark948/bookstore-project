import pytest

from shop.models import *


@pytest.mark.django_db
def test_country_fixture(country):
    print(country)