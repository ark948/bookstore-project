from django.urls import path

from . import views

urlpatterns = [
    path("browse/", views.browse, name='customers_browse'),
    path("", views.index, name='customers_index'),
]