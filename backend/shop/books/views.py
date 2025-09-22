from django.http.request import HttpRequest
from django.http.response import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
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
from shop.utils import has_custom_permission
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
    books_filter = BookFilter( data=request.GET, queryset=Book.objects.all() )
    paginator = Paginator( books_filter.qs, settings.PAGE_SIZE )
    page_obj = paginator.page(page)
    context = {
        'page_obj': page_obj,
        'filter': books_filter
    }
    if request.htmx:
        return render(request, "shop/books/partials/books-list-container.html", context)
    return render(request, "shop/books/books-list.html", context)


@role_required("employee")
def get_books(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page', 1)
    books_filter = BookFilter( data=request.GET, queryset=Book.objects.all() )
    paginator = Paginator( books_filter.qs, settings.PAGE_SIZE )
    page_obj = paginator.page(page)
    context = {
        'page_obj': page_obj,
        'filter': books_filter
    }
    # removed django-template-partial suffix from render statement and pagination was fixed
    return render(request, "shop/books/partials/books-list-container.html", context)


@role_required("employee")
def delete_book(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        book: Book = Book.objects.get(pk=pk)
        book.delete()
    except Book.DoesNotExist:
        if request.htmx:
            return HttpResponseNotFound("آیتم پیدا نشد.")
        else:
            return HttpResponseNotFound("آیتم پیدا نشد.")
    messages.info(request, "حذف انجام شد.")
    response = HttpResponse()
    response['HX-Redirect'] = reverse("shop:books-list")
    return response


@role_required("employee")
def book_details(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        item: Book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        pass
    response = render(request, "shop/books/book-details.html", {'item': item})
    return response


@role_required("employee")
def add_book(request: HttpRequest) -> HttpRequest:
    form = forms.BookForm()
    return render(request, "shop/books/add_book2.html", {'form': form })


@role_required("employee")
def edit_book(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "POST":
        pass
    book = get_object_or_404(Book, pk=pk)
    form = forms.BookForm(instance=book)
    return render(request, "shop/books/edit_book.html", { 'form': form })


@role_required("employee")
def request_book_for_editing(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        item_id = request.POST.get('input_field_name')
        if item_id is None:
            messages.error("خطا در دریافت شناسه.")
            return redirect("shop:edit-request")
        book_obj: Book = Book.objects.get(pk=item_id)
        if book_obj:
            form = forms.FullBookEditForm(instance=book_obj)
            response = render(request, "shop/books/partials/edit-book-form-full.html", {'form': form})
            return response
        else:
            return HttpResponse("متاسفانه کتاب یافت نشد یا وجود ندارد.")
    return render(request, 'shop/books/edit-book-page.html')


@role_required("employee")
def get_book_for_edit(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        try:
            item = Book.objects.get(pk=int(request.POST.get('input_field_name')))
        except Exception as e:
            return HttpResponse("شناسه یافت نشد.")
        form = forms.QuickBookEditForm(instance=item)
        response = render(request, "shop/books/partials/edit-book-form.html", {'form': form})
        return response


@role_required("employee")
def edit_book_process(request: HttpRequest, pk: int) -> HttpResponse:
    item: Book = Book.objects.get(pk=pk)
    if request.method == "POST":
        form = forms.QuickBookEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "آیتم بروزرسانی شد.")
            return redirect(reverse("shop:books-list"))
        else:
            return render(request, "shop/books/partials/edit-book-form.html", {'form': form})
        

@role_required("employee")
def load_edit_form_for_modal_container(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        item: Book = Book.objects.get(pk=pk)
    except Exception as error:
        messages.error(request, "خطایی رخ داد.")
        return redirect(reverse("shop:books-list"))
    form = forms.QuickBookEditForm(instance=item)
    response = render(request, "shop/books/forms/edit-book-form.html", {'form': form})
    return response


@role_required("employee")
def process_edit_form_from_modal(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        item: Book = Book.objects.get(pk=pk)
    except Exception as error:
        return HttpResponse("خطایی رخ داده است.")
    if request.method == "POST":
        form = forms.QuickBookEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            response = render(request, "shop/books/messages/successful-edit-with-modal.html", {'message': "بروزرسانی انجام شد."})
            response['HX-Trigger'] = "done"
            return response
        else:
            response = render(request, "shop/books/forms/edit-book-form.html", {'form': form})
            return response

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