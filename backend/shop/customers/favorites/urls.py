from django.urls import path

from shop.customers.favorites import views

urlpatterns = [
    path("check-favorite/<int:book_id>/", views.check_favorite_exists, name='check_favorite'),
    path("remove-from-favorites/<int:book_id>/", views.remove_book_favorite, name='remove_favorite'),
    path("add-to-favorite/<int:book_id>/", views.add_book_favorite, name='add_favorite'),
    path("is-book-favorite/<int:book_id>/", views.is_book_favorite, name='is_book_favorite'),
]