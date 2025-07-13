from django.urls import path

from .views import dashboards, books

app_name = "shop"

urlpatterns = [
    path("dashboard/admin/", dashboards.admin_dashboard, name='admin'),
    path("dashboard/manager/", dashboards.manager_dashboard, name='manager'),
    path("dashboard/employee/", dashboards.employee_dashboard, name='employee'),

    path("books/list/", books.books_list, name='books-list'),
    path("book/new/", books.add_book, name='add-book'),

    path("books/authors/load-authors/", books.load_authors_list, name='load-authors'),
]