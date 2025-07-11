from django.urls import path

from .views import base

app_name = "shop"

urlpatterns = [
    path("admin/", base.admin_dashboard, name='admin'),
    path("manager/", base.manager_dashboard, name='manager'),
    path("employee/", base.employee_dashboard, name='employee'),
]