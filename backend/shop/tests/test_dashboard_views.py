import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertRaisesMessage

from accounts.tests.conftest import user, custom_user, custom_employee, custom_manager, custom_admin


@pytest.mark.django_db
def test_admin_dashboard_inaccessible(custom_employee, client):
    response = client.get(reverse('shop:employee'))
    assert response.status_code == 403

@pytest.mark.django_db
def test_admin_dashboard(custom_employee, client):
    client.force_login(custom_employee)
    response = client.get(reverse('shop:employee'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_manager_dashboard_inaccessible(custom_employee, client):
    response = client.get(reverse('shop:manager'))
    assert response.status_code == 403

@pytest.mark.django_db
def test_manager_dashboard(custom_manager, client):
    client.force_login(custom_manager)
    response = client.get(reverse('shop:manager'))
    assert response.status_code == 200