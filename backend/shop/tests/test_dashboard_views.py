import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertRaisesMessage

from accounts.tests.conftest import user, custom_user, custom_employee, custom_manager, custom_admin


@pytest.mark.django_db
def test_admin_dashboard_inaccessible_by_employee(custom_employee, client):
    client.force_login(custom_employee)
    response = client.get(reverse('shop:admin'))
    assert response.status_code == 403

@pytest.mark.django_db
def test_admin_dashboard_inaccessible_by_manager(custom_manager, client):
    client.force_login(custom_manager)
    response = client.get(reverse("shop:admin"))
    assert response.status_code == 403

@pytest.mark.django_db
def test_admin_dashboard_accessible_only_to_admin(custom_admin, client):
    client.force_login(custom_admin)
    response = client.get(reverse('shop:admin'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_manager_dashboard_inaccessible_by_employee(custom_employee, client):
    client.force_login(custom_employee)
    response = client.get(reverse('shop:manager'))
    assert response.status_code == 403

@pytest.mark.django_db
def test_manager_dashboard_inaccessible_by_admin(custom_admin, client):
    client.force_login(custom_admin)
    response = client.get(reverse('shop:manager'))
    assert response.status_code == 403

@pytest.mark.django_db
def test_manager_dashboard_accessible_only_to_manager(custom_manager, client):
    client.force_login(custom_manager)
    response = client.get(reverse("shop:manager"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_employee_dashboard_inaccessible_by_user(custom_user, client):
    client.force_login(custom_user)
    response = client.get(reverse('shop:employee'))
    assert response.status_code == 403


@pytest.mark.django_db
def test_employee_dashboard_accessible_only_to_employee(custom_employee, client):
    client.force_login(custom_employee)
    response = client.get(reverse('shop:employee'))
    assert response.status_code == 200