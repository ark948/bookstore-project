from django.urls import path

from . import views

urlpatterns = [
    # CRUD Actions
    path("details/<int:pk>/", views.book_details, name='book-details'),
    path("delete/<int:pk>/", views.delete_book, name='delete-book'),
    path("<int:pk>/edit-process/", views.edit_book_process, name='edit-process'),
    path("edit-request/", views.request_book_for_editing, name='edit-request'),
    path("list/", views.books_list, name='books-list'),
    path("new/", views.add_book, name='add-book'),
    path("create/", views.book_creation_view, name='create-book'),
    path("add-book/", views.add_book_2, name='add_book2'),

    # Modals
    path("<int:pk>/edit-with-modal-process/", views.process_edit_form_from_modal, name='edit-modal-process'),
    path("<int:pk>/edit-with-modal/", views.load_edit_form_for_modal_container, name='load-for-edit'),

    # Form providers (partials)
    path("provide-new-form/", views.provide_new_book_form, name='prvd-new-book-form'),
    path("provide-books-list/", views.provide_books_list, name='prvd-books-list'),

    # Autocomplete routes (django-autocomplete-light)
    path("authors-autocomplete/", views.AuthorsAutoComplete.as_view(), name='authors-autocomplete'),
    path("publishers-autocomplete/", views.PublishersAutoComplete.as_view(), name='publishers-autocomplete'),
    path("genres-autocomplete/", views.GenresAutoComplete.as_view(), name='genres-autocomplete'),
    path("languages-autocomplete/", views.LanguageAutoComplete.as_view(), name='languages-autocomplete'),

    # Secret/Test routes
    path("test-view/", views.secret_view, name='secret'),
    path("secret-view/", views.secret_view_v2, name='secret-2'),
]