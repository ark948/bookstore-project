import pytest

from accounts.factories import CustomUserFactory
from accounts.models import CustomUser

@pytest.fixture
def user():
    return CustomUserFactory()


@pytest.fixture
def custom_user():
    user = CustomUser.objects.create(
        email='user1@email.com'
    )
    user.set_password('test123*A')
    user.save()
    return user