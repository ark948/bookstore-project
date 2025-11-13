from django.http.request import HttpRequest
from django.http.response import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.urls import reverse
from django.contrib import messages
from django.forms.models import model_to_dict
from typing import List
from django.db.models import QuerySet
from django.core.paginator import Paginator
from django.conf import settings
from django_htmx.http import retarget

from http import HTTPStatus

from dal import autocomplete

from shop.models import (
    Book,
    Author,
    Publication,
    Genre,
    Language,
)
from shop.books import forms
from accounts.decorators import role_required
from shop.utils import has_custom_permission, custom_print
from shop.books.filters import BookFilter


@user_passes_test(has_custom_permission, login_url='accounts:login')
def secret_view(request):
    return HttpResponse("Secret stuff")

@user_passes_test(lambda user: user.is_authenticated, login_url='accounts:login')
def secret_view_v2(request):
    return HttpResponse("Secret stuff 2")


@role_required("employee")
def books_list(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page', 1)
    books_filter = BookFilter( request.GET, queryset=Book.objects.all().order_by('created_at') )
    total = books_filter.qs.count()
    paginator = Paginator( books_filter.qs, settings.PAGE_SIZE )
    page_obj = paginator.page(page)
    context = {
        'total': total,
        'page_obj': page_obj,
        'filter': books_filter
    }
    if request.htmx:
        print("\nRequest is htmx\n")
        return render(request, "shop/books/partials/books-list-container.html", context)
    return render(request, "shop/books/books-list.html", context)


@role_required("employee")
def load_filtered_books(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        page = request.GET.get('page', 1)
        books_filter = BookFilter(
            request.GET,
            queryset=Book.objects.all()
        )
        results_count = books_filter.qs.count()
        paginator = Paginator( books_filter.qs, settings.PAGE_SIZE )
        page_obj = paginator.page(page)
        context = {
            'total': results_count,
            'page_obj': page_obj,
        }
        return render(request, "shop/books/partials/books-query.html", context)


@role_required("employee")
def get_books(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page', 1)
    books_filter = BookFilter( data=request.GET, queryset=Book.objects.all().order_by('created_at') )
    total = books_filter.qs.count()
    paginator = Paginator( books_filter.qs, settings.PAGE_SIZE )
    page_obj = paginator.page(page)
    context = {
        'total': total,
        'page_obj': page_obj,
        'filter': books_filter
    }
    # removed django-template-partial suffix from render statement and pagination was fixed
    return render(request, "shop/books/partials/books-list-container.html", context)


@role_required('employee')
def get_books_only(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page', 1)
    books_filter = BookFilter( data=request.GET, queryset=Book.objects.all().order_by('created_at') )
    total = books_filter.qs.count()
    paginator = Paginator( books_filter.qs, settings.PAGE_SIZE )
    page_obj = paginator.page(page)
    context = { 'total': total, 'page_obj': page_obj }
    return render(request, "shop/books/partials/books_list_only.html", context)



@require_POST
@role_required("employee")
def delete_book(request: HttpRequest, pk: int) -> HttpResponse:
    if request.htmx:
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        response = HttpResponse()
        response['HX-Trigger'] = 'successful_delete'
        return response
    

@role_required("employee")
def book_details(request: HttpRequest, pk: int) -> HttpResponse:
    book: Book = get_object_or_404(Book, pk=pk)
    return render(request, "shop/books/book-details.html", { 'item': book })


@role_required("employee")
def add_book(request: HttpRequest) -> HttpRequest:
    if request.method == "POST":
        form = forms.BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "کتاب با موفقیت افزوده شد.")
            return redirect(reverse("shop:books_list"))
        else:
            return render(request, "shop/books/add_book.html", { 'form': form })
    form = forms.BookForm()
    return render(request, "shop/books/add_book.html", { 'form': form })


@role_required("employee")
def edit_book(request: HttpRequest, pk: int) -> HttpResponse:
    book: Book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = forms.BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "ویرایش موفقیت آمیز بود.")
            return redirect(reverse('shop:books_list'))
        else:
            return render(request, "shop/books/edit_book.html", { 'form': form, 'item_id': pk })
    form = forms.BookForm(instance=book)
    return render(request, "shop/books/edit_book.html", { 'form': form, 'item_id': pk })


# This is not used, replaced by django-autocomplete-light
# But will remain for reference purposes
@role_required("employee")
def load_authors_list(request: HttpRequest) -> HttpResponse:
    authors_list_obj: QuerySet = Author.objects.all().order_by('fa_name', 'en_name')
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