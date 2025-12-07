from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import QuerySet
from django.db.utils import IntegrityError
from django.template.loader import render_to_string
from django.conf import settings

from accounts.decorators import role_required

from shop.models import (
    Book, Genre, Comment, Favorite
)
from accounts.models import CustomUser
from shop.customers.cart.cart import Cart
from shop.customers import filters
from shop.customers.cart.forms import ItemAddForm
from shop.customers.forms import (
    AddCommentForm
)


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "shop/customers/index.html", {})


def browse_books(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page', 1)
    books_filter = filters.BooksFilter(request.GET, queryset=Book.objects.all().order_by('created_at'))
    paginator = Paginator(books_filter.qs, settings.PAGE_SIZE)
    page_obj = paginator.page(page)
    total = books_filter.qs.count()
    return render(request, "shop/customers/browse_books.html", {
        'page_obj': page_obj,
        'filter': books_filter,
        'total': total
    })

def browse_books_only_available(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page', 1)
    books_filter = filters.BooksFilter(request.GET, queryset=Book.objects.filter(available=True).order_by('created_at'))
    paginator = Paginator(books_filter.qs, settings.PAGE_SIZE)
    page_obj = paginator.page(page)
    total = books_filter.qs.count()
    return render(request, "shop/customers/browse_books.html", {
        'page_obj': page_obj,
        'filter': books_filter,
        'total': total
    })


def item_detail(request: HttpRequest, id) -> HttpResponse:
    item: Book = get_object_or_404(Book, id=id)
    item_form = ItemAddForm()
    add_comment_form = AddCommentForm()
    is_favorited = False
    if request.user.is_authenticated and request.user.role == 'user':
        favorite = Favorite.objects.filter(user_id=request.user, book_id=item)
        if favorite:
            is_favorited = True
    return render(request, "shop/customers/item_details.html", {
            'is_fav': is_favorited,
            'item': item,
            'item_form': item_form, 
            'comment_form': add_comment_form
        })


@role_required('user')
def book_details(request: HttpRequest, book_id: int) -> HttpResponse:
    item: Book = get_object_or_404(Book, pk=book_id)
    item_form = ItemAddForm()
    add_comment_form = AddCommentForm()
    is_favorite = False
    context = {}
    if request.user.is_authenticated:
        favorite = Favorite.objects.filter(user_id=request.user, book_id=item)
        if favorite.exists():
            context['is_fav'] = is_favorite
        context['comment_form'] = add_comment_form
    context['item'] = item
    context['item_form'] = item_form
    if request.htmx:
        return render(request, "shop/customers/item_details_partial.html", context)
    return render(request, "shop/customers/item_details.html", context)
    

@require_POST
@role_required('user')
def add_comment(request: HttpRequest, book_id: int) -> HttpResponse:
    book = get_object_or_404(Book, id=book_id)
    form = AddCommentForm(request.POST)
    if form.is_valid():
        # if all data is available and no aciton is needed before saving object, use create()
        try:
            Comment.objects.create(
                title = form.cleaned_data['title'],
                body = form.cleaned_data['body'],
                book = book,
                user = request.user,
                anonymous = form.cleaned_data['anonymous']
            )
        except IntegrityError as unique_error:
            html = render_to_string('shop/customers/errors/forbidden.html', {
                'message': "شما قبلا برای این کتاب نظر ثبت کرده اید. در صورت نیاز لطفا آن را ویرایش کنید."
            })
            return HttpResponseForbidden(html)
        # return a single comment item
        # response = render(request, "shop/customers/partials/comment_item.html", {'comment': comment})
        # response['HX-Trigger'] = "comment_successfully_submitted"
        # in template, use hx-on:comment_successfully_submitted and hx-swap='beforeend' to listen to this event
        # and add the returned comment to the end of the list
        # return response
        return HttpResponse("نظر شما دریافت شد و پس از تایید نمایش داده خواهد شد.")
    else:
        # this needs to be upated with comment_form template
        messages.error(request, "خطایی در درج نظر رخ داد. لطفا دوباره تلاش کنید.")
        return HttpResponse(form.errors)


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


@role_required('user')
def load_book_comments(request: HttpRequest, book_id: int) -> HttpResponse:
    if request.htmx:
        try:
            comments = Comment.objects.filter(book=book_id, status="Approved")
        except Exception as error:
            return JsonResponse("متاسفانه خطایی رخ داده است. لطفا صفحه را مجددا رفرش کنید.")
        return render(request, "shop/customers/partials/book_item_comments.html", {'items': comments})


@role_required('employee')
def customers_list(request: HttpRequest) -> HttpResponse:
    customers = CustomUser.objects.filter(role='user').order_by('email')
    if request.htmx:
        return render(request, "shop/customers/list.html", {'customers': customers})
    return render(request, "shop/customers/pages/customers_list.html", {'customers': customers})