from django.urls import path

from . import views

urlpatterns = [
    path("cart-detail", views.cart_detail, name='cart_detail'),
    path("cart-add/<int:product_id>/", views.cart_add, name='cart_add'),
    path("remove/<int:product_id>/", views.cart_remove, name='cart_remove'),
    path("item-detail", views.item_detail, name='item_detail'),
    path("browse/", views.browse, name='customers_browse'),
    path("", views.index, name='customers_index'),
]