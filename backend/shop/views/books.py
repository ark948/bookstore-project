from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from shop.models import Book
from shop.forms import NewBookForm
from accounts.decorators import role_required


@role_required("employee")
def books_list(request: HttpRequest) -> HttpResponse:
    books_list_obj = Book.objects.all()
    context = {
        'books': books_list_obj
    }
    return render(request, "shop/books-list.html", context=context)


@role_required("employee")
def add_book(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        pass
    form = NewBookForm()
    context = {
        "form": form
    }
    return render(request, "shop/books/add-book.html", context=context)