import pytest

from shop.models import (
    Country, Language
)

@pytest.fixture
def country():
    us = Country.objects.create(name="United States")
    us.save()
    return us


@pytest.fixture
def language():
    en = Language.objects.create(name='English')
    en.save()
    return en