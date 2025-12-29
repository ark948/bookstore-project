from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet

from accounts.decorators import role_required
from shop.models import Book, Favorite


@role_required('user')
def is_book_favorite(request: HttpRequest, book_id: int) -> HttpResponse:
    if request.htmx:
        favorite: QuerySet = Favorite.objects.filter(user_id=request.user, book_id=book_id).first()
        if favorite:
            return render(request, "shop/customers/favorites/partials/remove_from_favorite_partial.html", {'book_id': book_id})
        else:
            return render(request, "shop/customers/favorites/partials/add_to_favorite_partial.html", {'book_id': book_id})
        

@role_required('user')
def is_book_favorite_for_book_details_page(request: HttpRequest, book_id: int) -> HttpResponse:
    if request.htmx:
        if Favorite.objects.filter(user_id=request.user, book_id=book_id).exists():
            return render(request, "shop/customers/favorites/partials/is_favorite.html", {'book_id': book_id})
        return render(request, "shop/customers/favorites/partials/not_favorite.html", {'book_id': book_id})
    

def add_book_favorite_details_page(request: HttpRequest, book_id: int) -> HttpResponse:
    book_obj = get_object_or_404(Book, pk=book_id)
    Favorite.objects.create(user_id=request.user, book_id=book_obj)
    return render(request, "shop/customers/favorites/partials/is_favorite.html", {'book_id': book_id})

def remove_book_favorite_details_page(request: HttpRequest, book_id: int) -> HttpResponse:
    Favorite.objects.filter(user_id=request.user, book_id=book_id).delete()
    return render(request, "shop/customers/favorites/partials/not_favorite.html", {'book_id': book_id})


@role_required('user')
def add_book_favorite(request: HttpRequest, book_id: int) -> HttpResponse:
    if request.htmx:
        book_obj = get_object_or_404(Book, pk=book_id)
        try:
            Favorite.objects.create(user_id=request.user, book_id=book_obj)
        except Exception as error:
            return HttpResponse("خطا")
        return render(request, "shop/customers/favorites/partials/remove_from_favorite_partial.html", {'book_id': book_id})
    

@role_required('user')
def remove_book_favorite(request: HttpRequest, book_id: int) -> HttpResponse:
    print("remove_book_favorite called")
    if request.htmx:
        print("request is htmx")
        book_obj = get_object_or_404(Book, pk=book_id)
        item = Favorite.objects.filter(user_id=request.user, book_id=book_obj).first()
        if item:
            print("item exists, deleting it...")
            item.delete()
        return render(request, "shop/customers/favorites/partials/add_to_favorite_partial.html", {'book_id': book_id})