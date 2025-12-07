from django.urls import path, include

from shop.customers.cart import urls as cart_urls
from shop.customers.books import urls as books_urls
from shop.customers.comments import urls as comments_urls
from shop.customers.favorites import urls as favorites_urls
from . import views

urlpatterns = [
    path('books/', include(books_urls)),
    path('comments/', include(comments_urls)),
    path('favorites/', include(favorites_urls)),
    path("cart/", include(cart_urls)),
    path('', views.index, name='customers_index'),

    path("list/", views.customers_list, name='customers_list'),
]