from django.urls import path, include

app_name = "shop"

urlpatterns = [
    path("books/", include("shop.books.urls")),
]