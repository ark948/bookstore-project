from django.http.request import HttpRequest
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.urls import reverse
from django.contrib import messages
from django.forms.models import model_to_dict
from typing import List
from django.db.models import QuerySet

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

@user_passes_test(lambda user: user.is_authenticated, login_url='accounts:login')
def secret_view_v2(request):
    return HttpResponse("Secret stuff 2")


@role_required("employee")
def books_list(request: HttpRequest) -> HttpResponse:
    books_list_obj: QuerySet = Book.objects.all()
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
def edit_book_request_page(request: HttpRequest) -> HttpResponse:
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