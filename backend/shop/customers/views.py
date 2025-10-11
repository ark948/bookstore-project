from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from accounts.decorators import role_required

from decimal import Decimal

from icecream import ic
ic.configureOutput(
    includeContext=False
)

from shop.models import (
    Book, Genre, Comment, Favorite
)
from accounts.models import CustomUser, UserProfile
from .cart import Cart
from .forms import (
    ItemAddForm,
    AddCommentForm
)


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "shop/customers/index.html", {})


def browse(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    genres = Genre.objects.all()
    return render(request, "shop/customers/browse.html", {
        'items': books,
        'genres': genres
    })


def provide_only_available_books(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        if request.GET.get('status'):
            books = Book.objects.filter(available=True)
        else:
            books = Book.objects.all()
    return render(request, "shop/customers/partials/books-container-section.html", {
        'items': books
    })


def item_detail(request: HttpRequest, id) -> HttpResponse:
    item = get_object_or_404(Book, id=id)
    item_form = ItemAddForm()
    add_comment_form = AddCommentForm()
    is_favorited = False
    if request.user.is_authenticated and request.user.role == 'user':
        favorite = Favorite.objects.filter(user_id=request.user, book_id=item)
        if favorite:
            is_favorited = True
    return render(request, "shop/customers/partials/book-item.html", {
            'is_fav': is_favorited,
            'item': item, 
            'item_form': item_form, 
            'comment_form': add_comment_form
        }
    )

@require_POST
def cart_add(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    if request.htmx:
        return HttpResponse("OK")
    cart = Cart(request)
    product: Book = get_object_or_404(Book, id=product_id)
    if not product.available:
        messages.error(request, "این کتاب موجود نیست.")
        return redirect(reverse("shop:customers_browse"))
    form = ItemAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product, 
            quantity=cd['quantity'], 
            override_quantity=cd['override']
        )
    return redirect(reverse("shop:cart_detail"))


@require_POST
def cart_remove(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)
    cart.remove(product)
    return redirect(reverse("shop:cart_detail"))


def cart_detail(request):
    cart = Cart(request)
    quantity_form = ItemAddForm()
    return render(request, "shop/customers/cart/detail.html", {'cart': cart, 'form': quantity_form})


@require_POST
def cart_update(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    cart = Cart(request)
    new_quantity = int(request.POST.get('quantity', 1))
    book = get_object_or_404(Book, id=product_id)
    cart.add(
        product=book,
        quantity=new_quantity,
        override_quantity=True
    )
    return redirect(reverse('shop:cart_detail'))


@require_POST
@role_required('user')
def add_comment(request: HttpRequest) -> HttpResponse:
    form = AddCommentForm(request.POST)
    if form.is_valid():
        comment_obj = Comment(
            body=form.cleaned_data['body'],
            book=get_object_or_404(Book, id=int(request.POST['book_id'])),
            user=request.user
        )
        comment_obj.save()
        return HttpResponse("نظر با موفقیت ثبت شد.")
    else:
        return HttpResponse(form.errors)
    

@role_required('user')
def get_number_of_cart_items(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    total = 0
    for i in cart:
        total += i['quantity']
    return HttpResponse(str(total))


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
    if request.htmx:
        term = request.GET.get('priceRange')
        books = Book.objects.filter(price__range=(0, Decimal(term))).all()
        return render(request, "shop/customers/partials/books-container-section.html", { 'items': books })
    else:
        books = Book.objects.all()
        return render(request, "shop/customers/partials/books-container-section.html", { 'items': books })
    

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
def add_book_to_favorites(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        book_id = request.GET.get('book_id')
        book_item = get_object_or_404(Book, id=book_id)
        if book_item:
            favorite = Favorite(user_id=request.user, book_id=book_item)
            favorite.save()
            response = render(request, "shop/customers/partials/remove_from_favorite_partial.html", {'book_id': book_id})
            return response
    else:
        return HttpResponse("add favorite ERROR")
    

@role_required('user')
def remove_book_from_favorites(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        book_id = request.GET.get('book_id')
        book_item = get_object_or_404(Book, id=book_id)
        favorite = Favorite.objects.filter(user_id=request.user, book_id=book_item)
        if favorite:
            favorite.delete()
            response = render(request, "shop/customers/partials/add_to_favorite_partial.html", {'book_id': book_id})
            return response
    else:
        return HttpResponse("remvoe favorite ERROR")
    

@role_required('user')
def is_book_in_user_favorites(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        book_id = request.GET.get('book_id')
        book_item = get_object_or_404(Book, id=book_id)
        favorite = Favorite.objects.filter(user_id=request.user, book_id=book_item).first()
        if favorite:
            response = render(request, "shop/customers/partials/remove_from_favorite_partial.html")
        else:
            response = render(request, "shop/customers/partials/add_to_favorite_partial.html")
        return response
    else:
        return HttpResponse("خطا")
    

@role_required('employee')
def customers_list(request: HttpRequest) -> HttpResponse:
    customers = CustomUser.objects.filter(role='user').order_by('email')
    return render(request, "shop/customers/customers/list.html", {'customers': customers})