import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertRaisesMessage
from pytest_lazy_fixtures import lf

from accounts.tests.conftest import user, custom_employee, custom_manager, custom_admin
from accounts.models import CustomUser

@pytest.mark.skip
@pytest.mark.django_db
@pytest.mark.parametrize("user_fixture, expected_status", [
    (lf("user"), 403),
    (lf("custom_employee") , 200),
])
def test_employee_dashboard(client, user_fixture, expected_status):

    client.force_login(user_fixture)
    response = client.get(reverse('shop:employee'))
    assert response.status_code == expected_status

@pytest.mark.skip
@pytest.mark.django_db
@pytest.mark.parametrize("user_fixture, expected_status", [
    (lf("user"), 403),
    (lf("custom_manager"), 200),
])
def test_manager_dashboard(client, user_fixture, expected_status):
    client.force_login(user_fixture)
    response = client.get(reverse('shop:manager'))
    assert response.status_code == expected_status

@pytest.mark.skip
@pytest.mark.django_db
@pytest.mark.parametrize("user_fixture, expected_status", [
    (lf("custom_employee"), 403),
    (lf("custom_manager"), 200),
])
def test_manager_dashboard_inaccessible_to_employee(client, user_fixture, expected_status):
    client.force_login(user_fixture)
    response = client.get(reverse("shop:manager"))
    assert response.status_code == expected_status

@pytest.mark.skip
@pytest.mark.django_db
@pytest.mark.parametrize("user_fixture, expected_status", [
    (lf("user"), 403),
    (lf("custom_admin"), 200),
])
def test_admin_dashboard(client, user_fixture, expected_status):
    client.force_login(user_fixture)
    response = client.get(reverse("shop:admin"))
    assert response.status_code == expected_status