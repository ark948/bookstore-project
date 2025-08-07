import pytest
import logging

from accounts.factories import CustomUserFactory, CustomEmployeeFactory
from accounts.models import CustomUser


@pytest.fixture(autouse=True)
def disable_logging_for_forbidden_requests(caplog):
    logger = logging.getLogger('django.request')
    logger.setLevel(logging.CRITICAL)
    yield
    logger.setLevel(logging.WARNING)


@pytest.fixture
def user():
    return CustomUserFactory()


@pytest.fixture
def custom_employee():
    return CustomEmployeeFactory()


@pytest.fixture
def users(user, employee):
    
    manager = CustomUser.objects.create(
        email='user_mgm@email.com',
        role='manager'
    )
    manager.set_password('test123*A')
    manager.save()

    admin = CustomUser.objects.create(
        email='user_adm@email.com',
        role='admin'
    )
    admin.set_password('test123*A')
    admin.save()

    return {
        'user': user,
        'employee': employee,
        'manager': manager,
        'admin': admin
    }
    