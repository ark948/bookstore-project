from django.urls import path

from .views import dashboards, books

app_name = "shop"

urlpatterns = [
    # CRUD Actions
    path("books/details/<int:pk>/", books.book_details, name='book-details'),
    path("bokos/delete/<int:pk>/", books.delete_book, name='delete-book'),
    path("books/<int:pk>/edit-process/", books.edit_book_process, name='edit-process'),
    path("books/edit-request/", books.request_book_for_editing, name='edit-request'),
    path("books/list/", books.books_list, name='books-list'),
    path("books/new/", books.add_book, name='add-book'),
    path("books/create/", books.book_creation_view, name='create-book'),

    # Modals
    path("books/<int:pk>/edit-with-modal-process/", books.process_edit_form_from_modal, name='edit-modal-process'),
    path("books/<int:pk>/edit-with-modal/", books.load_edit_form_for_modal_container, name='load-for-edit'),

    # Form providers (partials)
    path("books/provide-new-form/", books.provide_new_book_form, name='prvd-new-book-form'),
    path("books/provide-books-list/", books.provide_books_list, name='prvd-books-list'),

    # dashboard views
    path("dashboard/admin/", dashboards.admin_dashboard, name='admin'),
    path("dashboard/manager/", dashboards.manager_dashboard, name='manager'),
    path("dashboard/employee/", dashboards.employee_dashboard, name='employee'),

    # Autocomplete routes (django-autocomplete-light)
    path("books/authors-autocomplete/", books.AuthorsAutoComplete.as_view(), name='authors-autocomplete'),
    path("books/publishers-autocomplete/", books.PublishersAutoComplete.as_view(), name='publishers-autocomplete'),
    path("books/genres-autocomplete/", books.GenresAutoComplete.as_view(), name='genres-autocomplete'),
    path("books/languages-autocomplete/", books.LanguageAutoComplete.as_view(), name='languages-autocomplete'),

    # Secret/Test routes
    path("books/test-view/", books.secret_view, name='secret'),
    path("books/secret-view/", books.secret_view_v2, name='secret-2'),
]