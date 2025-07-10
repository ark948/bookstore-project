import pytest

from shop.models import *

@pytest.fixture
def country():
    us = Country.objects.create(name="United States")
    us.save()
    return us