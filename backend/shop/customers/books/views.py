from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.conf import settings

from accounts.decorators import role_required
from shop.models import Book, Genre, Favorite
from shop.customers import filters
from shop.customers.cart.forms import ItemAddForm
from shop.customers.forms import AddCommentForm


def browse_books(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page', 1)
    books_filter = filters.BooksFilter(
        request.GET, 
        queryset=Book.objects.all().order_by('created_at')
    )
    paginator = Paginator(books_filter.qs, settings.PAGE_SIZE)
    page_obj = paginator.page(page)
    total = books_filter.qs.count()
    return render(request, "shop/customers/books/browse.html", {
        'page_obj': page_obj,'filter': books_filter, 'total': total
    })


def browse_books_only_available(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page', 1)
    books_filter = filters.BooksFilter(
        request.GET, 
        queryset=Book.objects.filter(available=True).order_by('created_at')
    )
    paginator = Paginator(books_filter.qs, settings.PAGE_SIZE)
    page_obj = paginator.page(page)
    total = books_filter.qs.count()
    return render(request, "shop/customers/books/browse.html", {
        'page_obj': page_obj, 'filter': books_filter, 'total': total
    })


def item_detail(request: HttpRequest, id: int) -> HttpResponse:
    item: Book = get_object_or_404(Book, id=id)
    item_form = ItemAddForm()
    add_comment_form = AddCommentForm()
    is_favorited = False
    if request.user.is_authenticated and request.user.role == 'user':
        favorite = Favorite.objects.filter(user_id=request.user, book_id=item)
        if favorite:
            is_favorited = True
    return render(request, "shop/customers/item_details.html", {
            'is_fav': is_favorited, 'item': item, 'item_form': item_form,  'comment_form': add_comment_form
        })


def book_details(request: HttpRequest, book_id: int) -> HttpResponse:
    item: Book = get_object_or_404(Book, pk=book_id)
    item_form = ItemAddForm()
    add_comment_form = AddCommentForm()
    is_favorite = False
    context = {}
    if request.user.is_authenticated:
        context['comment_form'] = add_comment_form
        favorite = Favorite.objects.filter(user_id=request.user, book_id=item)
        if favorite.exists():
            context['is_fav'] = is_favorite
    context['item'] = item
    context['item_form'] = item_form
    if request.htmx:
        return render(request, "shop/customers/item_details_partial.html", context)
    return render(request, "shop/customers/item_details.html", context)


@role_required('user')
def filter_by_genre(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        term = request.GET.get('genreSelect')
        genres_list = list(Genre.objects.all())
        genres_list = [item.title for item in genres_list]
        if term and term in genres_list:
            books = Book.objects.filter(genres__title__exact=term).all()
            return render(request, "shop/customers/partials/books-container-section.html", { 'items': books })
        else:
            books = Book.objects.all()
            return render(request, "shop/customers/partials/books-container-section.html", { 'items': books })
    else:
        books = Book.objects.all()
        return render(request, "shop/customers/partials/books-container-section.html", { 'items': books })
    

@role_required('user')
def filter_by_price(request: HttpRequest) -> HttpResponse:
    term = request.GET.get('priceRange')
    items = Book.objects.filter(price__range=(0, Decimal(term)))
    return render(request, "shop/customers/items.html", {'items': items})
    

@role_required('user')
def search_books(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        term = request.GET.get('search')
        books = Book.objects.filter(title__icontains=term).all()
        return render(request, "shop/customers/partials/books-container-section.html", { 'items': books })
    else:
        books = Book.objects.all()
        return render(request, "shop/customers/partials/books-container-section.html", { 'items': books })
    

@role_required('user')
def load_books(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    return render(request, "shop/customers/partials/books-container-section.html", { 'items': books })
