from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import QuerySet
from django.db.utils import IntegrityError
from django.template.loader import render_to_string

from accounts.decorators import role_required

from decimal import Decimal

# from icecream import ic
# ic.configureOutput(
#     includeContext=False
# )

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


def provide_only_available_books2(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        books = Book.objects.all()
        if request.GET.get('availability_status_field'):
            books = books.filter(available=True)
        return render(request, "shop/customers/partials/books-container-section.html", {
            'items': books
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


def book_details(request: HttpRequest, book_id: int) -> HttpResponse:
    item = Book = get_object_or_404(Book, pk=book_id)
    item_form = ItemAddForm()
    add_comment_form = AddCommentForm()
    is_favorite = False
    context = {}
    if request.user.is_authenticated and request.user.role == "user":
        favorite = Favorite.objects.filter(user_id=request.user, book_id=item)
        if favorite.exists():
            context['is_fav'] = is_favorite
        context['comment_form'] = add_comment_form
    context['item'] = item
    context['item_form'] = item_form
    return render(request, "shop/customers/item_details.html", context)
    


@require_POST
def cart_add(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    product: Book = get_object_or_404(Book, id=product_id)
    cart = Cart(request)
    if request.htmx:
        cart.add(
            product=product,
            quantity=1,
        )
        response = render(request, "shop/customers/partials/remove_from_cart.html", {})
        response['HX-Trigger'] = 'quick_add_success'
        return response
    if not product.available:
        messages.error(request, "این کتاب موجود نیست.")
        return redirect(reverse("shop:customers_browse"))
    if not product.copies_available > 0:
        messages.error(request, "متاسفانه موجودی این کتاب کافی نیست.")
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
def cart_clear(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    cart.clear()
    return redirect(reverse("shop:cart_detail"))


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