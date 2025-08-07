import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertRaisesMessage

from accounts.tests.conftest import users
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



@pytest.mark.django_db
@pytest.mark.parametrize("role, expected_status", [
    ("user", 403),
    ("manager", 200)
])
def test_manager_dashboard(client, role, expected_status):
    user = CustomUser.objects.create(
        email='manager@example.com',
        password='test123*A',
        role=role
    )

    client.force_login(user)
    response = client.get(reverse('shop:manager'))
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
