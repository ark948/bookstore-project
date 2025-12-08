from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import QuerySet

from accounts.decorators import role_required
from shop.models import Book, Favorite
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



def book_details(request: HttpRequest, book_id: int) -> HttpResponse:
    context = {}
    item: Book = get_object_or_404(Book, pk=book_id)
    if item.available:
        if item.copies_available >= 1:
            item_form = ItemAddForm()
            context['item_form'] = item_form
    add_comment_form = AddCommentForm()
    is_favorite = False
    if request.user.is_authenticated and request.user.role == 'user':
        context['comment_form'] = add_comment_form
        favorite = Favorite.objects.filter(user_id=request.user, book_id=item)
        if favorite.exists():
            context['is_fav'] = is_favorite
    context['item'] = item
    return render(request, "shop/customers/books/book_item_details_page.html", context)

    

@role_required('user')
def filter_by_price(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        term = request.GET.get('priceRange')
        page = request.GET.get('page', 1)
        books: QuerySet = Book.objects.filter(price__range=(0, Decimal(term)))
        paginator = Paginator(books, settings.PAGE_SIZE)
        page_obj = paginator.page(page)
        return render(
            request, 
            "shop/customers/books/partials/book_cards_section_partial.html", 
            {'page_obj': page_obj}
        )
    

@role_required('user')
def search_books(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        term = request.GET.get('search')
        page = request.GET.get('page', 1)
        books: QuerySet = Book.objects.filter(title__icontains=term).all()
        paginator = Paginator(books, settings.PAGE_SIZE)
        page_obj = paginator.page(page)
        return render(
            request, 
            "shop/customers/books/partials/book_cards_section_partial.html", 
            {'page_obj': page_obj}
        )
    

@role_required('user')
def refresh(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page', 1)
    books: QuerySet = Book.objects.all()
    paginator = Paginator(books, settings.PAGE_SIZE)
    page_obj = paginator.page(page)
    if request.htmx:
        return render(request,
            "shop/customers/books/partials/book_cards_section_partial.html",
            {'page_obj': page_obj}
        )
    return redirect(reverse('shop:browse_books'))
