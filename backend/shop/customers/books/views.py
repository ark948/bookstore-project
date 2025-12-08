from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import QuerySet

from accounts.decorators import role_required
from shop.models import Book, Favorite
from shop.customers import filters
from shop.customers.cart.forms import ItemAddForm
from shop.customers.forms import AddCommentForm

# OK
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


# OK
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


# OK
def book_details(request: HttpRequest, book_id: int) -> HttpResponse:
    item: Book = get_object_or_404(Book, pk=book_id)
    item_form = ItemAddForm()
    add_comment_form = AddCommentForm()
    is_favorite = False
    context = {}
    if request.user.is_authenticated and request.user.role == 'user':
        context['comment_form'] = add_comment_form
        favorite = Favorite.objects.filter(user_id=request.user, book_id=item)
        if favorite.exists():
            context['is_fav'] = is_favorite
    context['item'] = item
    context['item_form'] = item_form
    return render(request, "shop/customers/books/book_item_details_page.html", context)

    
# OK
@role_required('user')
def filter_by_price(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        term = request.GET.get('priceRange')
        page = request.GET.get('page', 1)
        items: QuerySet = Book.objects.filter(price__range=(0, Decimal(term)))
        paginator = Paginator(items, settings.PAGE_SIZE)
        page_obj = paginator.page(page)
        return render(
            request, 
            "shop/customers/books/partials/book_cards_section_partial.html", 
            {'page_obj': page_obj}
        )
    

# OK
@role_required('user')
def search_books(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        term = request.GET.get('search')
        page = request.GET.get('page', 1)
        items: QuerySet = Book.objects.filter(title__icontains=term).all()
        paginator = Paginator(items, settings.PAGE_SIZE)
        page_obj = paginator.page(page)
        return render(
            request, 
            "shop/customers/books/partials/book_cards_section_partial.html", 
            { 'page_obj': page_obj }
        )
    

@role_required('user')
def load_books(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    return render(request, "shop/customers/partials/books-container-section.html", { 'items': books })
