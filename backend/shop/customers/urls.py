from django.urls import path, include

from shop.customers.cart import urls as cart_urls
from shop.customers.books import urls as books_urls
from shop.customers.comments import urls as comments_urls
from . import views

urlpatterns = [
    # favorite related controls
    path("remove-from-favorites/<int:book_id>/", views.remove_book_favorite, name='remove_favorite'),
    path("add-to-favorite/<int:book_id>/", views.add_book_favorite, name='add_favorite'),
    path('is-book-favorite/<int:book_id>/', views.is_book_favorite, name='is_book_favorite'),

    # routes for employees
    path("list/", views.customers_list, name='customers_list'),
    path('books/', include(books_urls)),
    path('comments/', include(comments_urls)),
    path("cart/", include(cart_urls)),
    path('', views.index, name='customers_index'),
]