from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from shop.models import Book


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "shop/customers/index.html", {})


def browse(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    return render(request, "shop/customers/browse.html", {"items": books})