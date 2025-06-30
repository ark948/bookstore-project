import pytest

from accounts.factories import CustomUserFactory
from accounts.models import CustomUser

@pytest.fixture
def user():
    return CustomUserFactory()