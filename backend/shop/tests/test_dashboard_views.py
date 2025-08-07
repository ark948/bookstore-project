import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertRaisesMessage
from pytest_lazy_fixtures import lf

from accounts.tests.conftest import users, custom_employee
from accounts.models import CustomUser


@pytest.mark.django_db
@pytest.mark.parametrize("role, expected_status", [
    ("user", 403),
    ("employee", 200),
])
def test_employee_dashboard(client, role, expected_status):
    user = CustomUser.objects.create_user(
        email='some@example.com',
        password='test123*A',
        role=role
    )

    client.login(email=user.email, password='test123*A')
    response = client.get(reverse('shop:employee'))
    assert response.status_code == expected_status


@pytest.fixture
def user():
    return CustomUser.objects.create_user(email='user@example.com', password="pass", role="user")

@pytest.fixture
def manager_user():
    return CustomUser.objects.create_user(email='manager@example.com', password="pass", role="manager")

@pytest.fixture
def employee_user():
    return CustomUser.objects.create_user(email='employee@email.com', password="pass", role="employee")


@pytest.mark.django_db
@pytest.mark.parametrize("user_fixture, expected_status", [
    (lf('user'), 403),
    (lf('employee_user'), 200),
])
def test_manager_dashboard(client, user_fixture, expected_status):
    client.force_login(user_fixture)
    response = client.get(reverse('shop:employee'))
    assert response.status_code == expected_status


# import pytest
# # from pytest_lazyfixture import lazy_fixture

# @pytest.mark.django_db
# @pytest.mark.parametrize("user_fixture, expected_status", [
#     (lazy_fixture('admin_user'), 200),
#     (lazy_fixture('manager_user'), 200),
#     (lazy_fixture('employee_user'), 403),
# ])
# def test_access_roles(client, user_fixture, expected_status):
#     client.login(username=user_fixture.username, password="pass")
#     url = reverse("your_protected_view")
#     response = client.get(url)
#     assert response.status_code == expected_status
