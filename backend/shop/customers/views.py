from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet

from accounts.decorators import role_required
from shop.models import Book, Favorite
from accounts.models import CustomUser


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "shop/customers/index.html", {})


    
@role_required('user')
def add_book_favorite(request: HttpRequest, book_id: int) -> HttpResponse:
    if request.htmx:
        book_obj = get_object_or_404(Book, pk=book_id)
        try:
            Favorite.objects.create( user_id=request.user, book_id = book_obj )
        except Exception as error:
            print("\nERROR:", error, "\n")
            return HttpResponse("خطا")
        return render(request, "shop/customers/partials/remove_from_favorite_partial.html", {'book_id': book_id})
    

@role_required('user')
def remove_book_favorite(request: HttpRequest, book_id: int) -> HttpResponse:
    if request.htmx:
        book_obj = get_object_or_404(Book, pk=book_id)
        # using delete() is more efficient, than acquiring the obj with first() and the deleting it
        # delete() reuturns a tuple of num_deleted, deleted_details
        Favorite.objects.filter( user_id=request.user, book_id=book_obj ).delete()
        return render(request, "shop/customers/partials/add_to_favorite_partial.html", {'book_id': book_id})
    

@role_required('user')
def is_book_favorite(request: HttpRequest, book_id: int) -> HttpResponse:
    if request.htmx:
        favorite: QuerySet = Favorite.objects.filter( user_id=request.user, book_id=book_id ).first()
        if favorite:
            return render(request, "shop/customers/partials/remove_from_favorite_partial.html", {'book_id': book_id})
        return render(request, "shop/customers/partials/add_to_favorite_partial.html", {'book_id': book_id})


@role_required('employee')
def customers_list(request: HttpRequest) -> HttpResponse:
    customers = CustomUser.objects.filter(role='user').order_by('email')
    if request.htmx:
        return render(request, "shop/customers/list.html", {'customers': customers})
    return render(request, "shop/customers/pages/customers_list.html", {'customers': customers})