from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from dal import autocomplete

from shop.models import (
    Book,
    Author,
    Publication,
    Genre,
    Language,
)
from shop.forms import NewBookForm
from accounts.decorators import role_required


@role_required("employee")
def books_list(request: HttpRequest) -> HttpResponse:
    books_list_obj = Book.objects.all()
    context = {
        'books': books_list_obj
    }
    return render(request, "shop/books/books-list.html", context=context)


@role_required("employee")
def add_book(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        pass
    form = NewBookForm()
    context = {
        "form": form
    }
    return render(request, "shop/books/add-book.html", context=context)


@role_required("employee")
def load_authors_list(request: HttpRequest):
    authors_list_obj = Author.objects.all()
    response = render(request, "shop/books/partials/authors-list.html", {'authors': authors_list_obj})
    return response


@role_required("employee")
def add_book_test(request):
    form = NewBookForm()
    if request.method == "POST":
        print("\n\n", request.POST, "\n\n")
        form = NewBookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "با موفقیت افزوده شد.")
            return redirect(reverse('shop:books-list'))
        return render(request, "shop/books/add-book-test.html", context={
            'form': form
        })
    context = { "form": form }
    return render(request, "shop/books/add-book-test.html", context=context)


@role_required("employee")
def edit_book_test(request):
    return None


class AuthorsAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Author.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
    
class PublishersAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Publication.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
    
class GenresAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):        
        qs = Genre.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
    
class LanguageAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Language.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs