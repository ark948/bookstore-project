from django.urls import path

from . import views

urlpatterns = [
    # cart actions
    path("cart-update/<int:product_id>/", views.cart_update, name='cart_update'),
    path("cart-detail/", views.cart_detail, name='cart_detail'),
    path("cart-add/<int:product_id>/", views.cart_add, name='cart_add'),
    path("cart-remove/<int:product_id>/", views.cart_remove, name='cart_remove'),

    path("item-add-comment/", views.add_comment, name='add_comment'),
    path("item-detail/<int:id>/", views.item_detail, name='item_detail'),
    path("browse/", views.browse, name='customers_browse'),
    path("", views.index, name='customers_index'),

    # loaders
    path("load-books/", views.load_books, name='load_books'),
    path("get-cart-count/", views.get_number_of_cart_items, name='cart_count'),

    # search
    path("search/", views.search_books, name='search'),

    # filters
    path("filter-price/", views.filter_by_price, name='filter_price'),
    path("filter-genre/", views.filter_by_genre, name='filter_genre'),
    path("browse-only-available/", views.provide_only_available_books, name='only_available'),
]