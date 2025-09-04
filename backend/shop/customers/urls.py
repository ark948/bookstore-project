from django.urls import path

from . import views

urlpatterns = [
    path('item-add-comment/', views.add_comment, name='add_comment'),
    path('cart-update/<int:product_id>/', views.cart_update, name='cart_update'),
    path("cart-detail/", views.cart_detail, name='cart_detail'),
    path("cart-add/<int:product_id>/", views.cart_add, name='cart_add'),
    path("remove/<int:product_id>/", views.cart_remove, name='cart_remove'),
    path("item-detail/<int:id>/", views.item_detail, name='item_detail'),
    path("browse/", views.browse, name='customers_browse'),
    path("", views.index, name='customers_index'),

    # info loaders
    path('get-cart-count/', views.get_number_of_cart_items, name='cart_count'),

    # filters
    path('filter-by-price/', views.filter_by_price, name='filter_price'),
    path('filter-by-genre/', views.filter_by_genre, name='filter_genre'),
    path('browse-only-available/', views.provide_only_available_books, name='only_available'),
]