from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages

from accounts.decorators import role_required

from decimal import Decimal

from icecream import ic
ic.configureOutput(
    includeContext=False
)

from shop.models import (
    Book, Genre, Comment
)
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


def item_detail(request, id):
    item = get_object_or_404(Book, id=id)
    item_form = ItemAddForm()
    add_comment_form = AddCommentForm()
    return render(request,
                  "shop/customers/partials/book-item.html", {
                      'item': item, 
                      'item_form': item_form, 
                      'comment_form': add_comment_form})

@require_POST
def cart_add(request: HttpRequest, product_id):
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
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)
    cart.remove(product)
    return redirect(reverse("shop:cart_detail"))


def cart_detail(request):
    cart = Cart(request)
    quantity_form = ItemAddForm()
    return render(request, "shop/customers/cart/detail.html", {'cart': cart, 'form': quantity_form})


@require_POST
def cart_update(request: HttpRequest, product_id):
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