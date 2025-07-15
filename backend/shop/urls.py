from django.urls import path

from .views import dashboards, books

app_name = "shop"

urlpatterns = [
    path("dashboard/admin/", dashboards.admin_dashboard, name='admin'),
    path("dashboard/manager/", dashboards.manager_dashboard, name='manager'),
    path("dashboard/employee/", dashboards.employee_dashboard, name='employee'),

    path("books/list/", books.books_list, name='books-list'),
    path("book/new/", books.add_book, name='add-book'),
    path("book/new-test/", books.add_book_test, name='add-book-test'),

    path("books/authors/load-authors/", books.load_authors_list, name='load-authors'),
    path("books/authors-autocomplete/", books.AuthorsAutoComplete.as_view(), name='authors-autocomplete'),
    path("books/publishers-autocomplete/", books.PublishersAutoComplete.as_view(), name='publishers-autocomplete'),
    path("books/genres-autocomplete/", books.GenresAutoComplete.as_view(), name='genres-autocomplete'),
    path("books/languages-autocomplete/", books.LanguageAutoComplete.as_view(), name='languages-autocomplete'),
]