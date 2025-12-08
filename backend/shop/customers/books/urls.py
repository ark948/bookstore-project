from django.urls import path

from shop.customers.books import views

urlpatterns = [
    path("book-details/<int:book_id>/", views.book_details, name='customers_book_details'),

    path("browse-books-only-available/", views.browse_books_only_available, name="browse_books_only_available"),
    path("load-books/", views.load_books, name='load_books'),
    path("search/", views.search_books, name='search'),
    path("filter-price/", views.filter_by_price, name='filter_price'),

    path("browse-books/", views.browse_books, name='browse_books'),
]