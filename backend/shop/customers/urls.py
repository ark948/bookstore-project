from django.urls import path

from . import views

urlpatterns = [
    path("cart-detail", views.cart_detail, name='cart-detail'),
    path("cart-add/<int:product_id>/", views.cart_add, name='cart-add'),
    path("remove/<int:product_id>/", views.cart_remove, name='cart-remove'),
    path("browse/", views.browse, name='customers_browse'),
    path("", views.index, name='customers_index'),
]