from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.urls import reverse
from django.contrib import messages
from django.forms.models import model_to_dict
from typing import List

from dal import autocomplete

from shop.models import (
    Book,
    Author,
    Publication,
    Genre,
    Language,
)
from shop import forms
from accounts.decorators import role_required


def has_custom_permission(user):
    return user.is_authenticated

@user_passes_test(has_custom_permission, login_url='accounts:login')
def secret_view(request):
    return HttpResponse("Secret stuff")


@role_required("employee")
def books_list(request: HttpRequest) -> HttpResponse:
    books_list_obj: Book = Book.objects.all()
    return render(request, "shop/books/books-list.html", context={ 'books': books_list_obj })


@role_required("employee")
def add_book(request: HttpRequest) -> HttpResponse:
    form = forms.NewBookForm()
    if request.method == "POST":
        form = forms.NewBookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "کتاب با موفقیت افوزده شد.")
            return redirect(reverse("shop:books-list"))
        return render(request, "shop/books/add-book.html", context={ 'form': form })
    return render(request, "shop/books/add-book.html", context={ "form": form })


@role_required("employee")
def add_book_test(request: HttpRequest) -> HttpResponse:
    form = forms.NewBookForm()
    if request.method == "POST":
        form = forms.NewBookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "با موفقیت افزوده شد.")
            return redirect(reverse('shop:books-list'))
        return render(request, "shop/books/add-book-test.html", context={ 'form': form })
    return render(request, "shop/books/add-book-test.html", context={ "form": form })


@role_required("employee")
def edit_book_test(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        item: Book = Book.objects.get(pk)
    except Exception:
        messages.error(request, "شناسه یافت نشد.")
        return redirect(reverse("books:books-list")) # update if htmx was used
    if request.method == "POST":
        form = forms.EditBookForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"کتاب با موفقیت ویرایش شد. {pk}")
            return redirect(reverse("books:books-list")) # update if htmx was used
        else:
            return render(request, "shop/books/edit-book.html", { 'form': form })
    form = forms.EditBookForm(initial=model_to_dict(item))
    return render(request, "shop/books/edit-book.html", { 'form': form })
        


# This is not used, replaced by django-autocomplete-light
# But will remain for reference purposes
@role_required("employee")
def load_authors_list(request: HttpRequest) -> HttpResponse:
    authors_list_obj: List[Author] = Author.objects.all().order_by('fa_name', 'en_name')
    return render(request, "shop/books/partials/authors-list.html", {'authors': authors_list_obj})


class AuthorsAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Author.objects.all().order_by('fa_name', 'en_name')
        if self.q:
            qs = qs.filter(en_name__istartswith=self.q)
        return qs
    
class PublishersAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Publication.objects.all().order_by('title')
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs
    
class GenresAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):        
        qs = Genre.objects.all()
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs
    
class LanguageAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Language.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs