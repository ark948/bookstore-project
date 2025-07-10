import pytest

from shop.models import *


# OK
@pytest.mark.skip
@pytest.mark.django_db
def test_country_fixture(country):
    print(country)
    print(country.pk)
    print(country.name)


# OK
@pytest.mark.skip
@pytest.mark.django_db
def test_langauge_fixtre(language):
    print(language)
    print(language.pk)
    print(language.name)