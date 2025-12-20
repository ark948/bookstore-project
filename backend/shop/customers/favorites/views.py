from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet

from accounts.decorators import role_required
from shop.models import Book, Favorite


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
    if request.htmx:
        book_obj = get_object_or_404(Book, pk=book_id)
        Favorite.objects.filter(user_id=request.user, book_id=book_obj).delete()
        return render(request, "shop/customers/favorites/partials/add_to_favorite_partial.html", {'book_id': book_id})
    

@role_required('user')
def is_book_favorite(request: HttpRequest, book_id: int) -> HttpResponse:
    if request.htmx:
        favorite: QuerySet = Favorite.objects.filter(user_id=request.user, book_id=book_id).first()
        if favorite:
            return render(request, "shop/customers/favorites/partials/remove_from_favorite_partial.html", {'book_id': book_id})
        else:
            return render(request, "shop/customers/favorites/partials/add_to_favorite_partial.html", {'book_id': book_id})