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
def test_employee_dashboard(client, CustomUser, role, expected_status):
    user = CustomUser.objects.create_user(
        email='some@example.com',
        password='test123*A',
        role=role
    )

    client.login(email=user.email, password='test123*A')
    response = client.get(reverse('shop:employee'))
    assert response.status_code == expected_status


############################################################ Consider using:
# (For testing the RBAC system)
# Here is our RBAC decorator: 
# from django.http import HttpResponseForbidden
# from functools import wraps

# def role_required(allowed_roles):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             if request.user.role not in allowed_roles:
#                 return HttpResponseForbidden("Not allowed")
#             return view_func(request, *args, **kwargs)
#         return _wrapped_view
#     return decorator


# # Here are fixtures
# import pytest

# @pytest.fixture
# def admin_user(django_user_model):
#     return django_user_model.objects.create_user(username="admin", password="pass", role="admin")

# @pytest.fixture
# def manager_user(django_user_model):
#     return django_user_model.objects.create_user(username="manager", password="pass", role="manager")

# @pytest.fixture
# def employee_user(django_user_model):
#     return django_user_model.objects.create_user(username="employee", password="pass", role="employee")

# # import pytest
# # # from pytest_lazyfixture import lazy_fixture

# # @pytest.mark.django_db
# # @pytest.mark.parametrize("user_fixture, expected_status", [
# #     (lazy_fixture('admin_user'), 200),
# #     (lazy_fixture('manager_user'), 200),
# #     (lazy_fixture('employee_user'), 403),
# # ])
# # def test_access_roles(client, user_fixture, expected_status):
# #     client.login(username=user_fixture.username, password="pass")
# #     url = reverse("your_protected_view")
# #     response = client.get(url)
# #     assert response.status_code == expected_status
