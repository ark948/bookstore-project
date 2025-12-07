from django.urls import path

from shop.customers.cart import views

urlpatterns = [
    path("cart-update/<int:product_id>/", views.cart_update, name='cart_update'),
    path("cart-detail/", views.cart_detail, name='cart_detail'),
    path("cart-add/<int:product_id>/", views.cart_add, name='cart_add'),
    path("cart-remove/<int:product_id>/", views.cart_remove, name='cart_remove'),
    path("cart-clear/", views.cart_clear, name='cart_clear'),
    path("get-cart-count/", views.get_number_of_cart_items, name='cart_count'),
]