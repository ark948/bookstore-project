from django.urls import path

from .views import dashboards, books

app_name = "shop"

urlpatterns = [
    # dashboard views
    path("dashboard/admin/", dashboards.admin_dashboard, name='admin'),
    path("dashboard/manager/", dashboards.manager_dashboard, name='manager'),
    path("dashboard/employee/", dashboards.employee_dashboard, name='employee'),

    # books views
    path("books/<int:pk>/edit-with-modal-process/", books.process_edit_form_from_modal, name='edit-modal-process'),
    path("books/<int:pk>/edit-with-modal/", books.load_edit_form_for_modal_container, name='load-for-edit'),
    path("books/<int:pk>/edit-process/", books.edit_book_process, name='edit-process'),
    path("books/get-book-for-edit/", books.get_book_for_edit, name='get-book'),
    path("books/edit-request/", books.edit_book_request_page, name='edit-request'),
    path("books/test-view/", books.secret_view, name='secret'),
    path("books/secret-view/", books.secret_view_v2, name='secret-2'),
    path("books/list/", books.books_list, name='books-list'),
    path("book/new/", books.add_book, name='add-book'),
    path("book/new-test/", books.add_book_test, name='add-book-test'),

    # Autocomplete fields (django-autocomplete-light)
    path("books/authors/load-authors/", books.load_authors_list, name='load-authors'),
    path("books/authors-autocomplete/", books.AuthorsAutoComplete.as_view(), name='authors-autocomplete'),
    path("books/publishers-autocomplete/", books.PublishersAutoComplete.as_view(), name='publishers-autocomplete'),
    path("books/genres-autocomplete/", books.GenresAutoComplete.as_view(), name='genres-autocomplete'),
    path("books/languages-autocomplete/", books.LanguageAutoComplete.as_view(), name='languages-autocomplete'),
]