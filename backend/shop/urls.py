from django.urls import path

from .views import dashboards

app_name = "shop"

urlpatterns = [
    path("admin/", dashboards.admin_dashboard, name='admin'),
    path("manager/", dashboards.manager_dashboard, name='manager'),
    path("employee/", dashboards.employee_dashboard, name='employee'),
]