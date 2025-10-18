from django.urls import path

from . import views

urlpatterns = [
    # routes for employees
    path("list/", views.customers_list, name='customers_list'),

    # cart actions
    path("cart-update/<int:product_id>/", views.cart_update, name='cart_update'),
    path("cart-detail/", views.cart_detail, name='cart_detail'),
    path("cart-add/<int:product_id>/", views.cart_add, name='cart_add'),
    path("cart-remove/<int:product_id>/", views.cart_remove, name='cart_remove'),

    # other
    path("add-comment/<int:book_id>/", views.add_comment, name='add_comment'),
    path("remove-from-favorites/<int:book_id>/", views.remove_book_favorite, name='remove_favorite'),
    path("add-to-favorite/<int:book_id>/", views.add_book_favorite, name='add_favorite'),
    path("item-detail/<int:id>/", views.item_detail, name='item_detail'),
    path("browse/", views.browse, name='customers_browse'),
    path("", views.index, name='customers_index'),

    # loaders
    path('load-book-comments/<int:book_id>/', views.load_book_comments, name='load_book_comments'),
    path('is-book-favorite/<int:book_id>/', views.is_book_favorite, name='is_book_favorite'),
    path("load-books/", views.load_books, name='load_books'),
    path("get-cart-count/", views.get_number_of_cart_items, name='cart_count'),

    # search
    path("search/", views.search_books, name='search'),

    # filters
    path("filter-price/", views.filter_by_price, name='filter_price'),
    path("filter-genre/", views.filter_by_genre, name='filter_genre'),
    path("browse-only-available/", views.provide_only_available_books, name='only_available'),
]