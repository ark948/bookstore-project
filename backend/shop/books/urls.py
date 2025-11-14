from django.urls import path

from . import views

urlpatterns = [
    # CRUD Actions
    path("details/<int:pk>/", views.book_details, name='book_details'),
    path("delete/<int:pk>/", views.delete_book, name='delete_book'),
    path("list/", views.books_list, name='books_list'),
    path("create/", views.add_book, name='add_book'),
    path("edit/<int:pk>/", views.edit_book, name='edit_book'),

    path("authors/list/", views.authors_list, name='authors_list'),
    path("genres/list/", views.genres_list, name='genres_list'),
    path("publications/list/", views.publications_list, name='publications_list'),
    path("translators/list/", views.translators_list, name="translators_list"),

    # partials
    path("get-books/", views.get_books, name='get_books'),
    path("filter-books/", views.load_filtered_books, name='load_filter'),
    path("get-books-only/", views.get_books_only, name='get_books_only'),

    # Autocomplete routes (django-autocomplete-light)
    path("authors-autocomplete/", views.AuthorsAutoComplete.as_view(), name='authors-autocomplete'),
    path("publishers-autocomplete/", views.PublishersAutoComplete.as_view(), name='publishers-autocomplete'),
    path("genres-autocomplete/", views.GenresAutoComplete.as_view(), name='genres-autocomplete'),
    path("languages-autocomplete/", views.LanguageAutoComplete.as_view(), name='languages-autocomplete'),

    # Secret/Test routes
    path("test-view/", views.secret_view, name='secret'),
    path("secret-view/", views.secret_view_v2, name='secret-2'),
]