from django.urls import path, include

from .views import dashboards

app_name = "shop"

urlpatterns = [
    path("books/", include("shop.books.urls")),

    # dashboard views
    path("dashboard/admin/", dashboards.admin_dashboard, name='admin'),
    path("dashboard/manager/", dashboards.manager_dashboard, name='manager'),
    path("dashboard/employee/", dashboards.employee_dashboard, name='employee'),
]