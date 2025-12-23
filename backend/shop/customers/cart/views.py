from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib import messages

from accounts.decorators import role_required

from shop.models import Book
from shop.customers.cart.cart import Cart
from shop.customers.cart.forms import ItemAddForm


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
        return redirect(reverse("shop:browse_books"))
    if not product.copies_available > 0:
        messages.error(request, "متاسفانه موجودی این کتاب کافی نیست.")
        return redirect(reverse("shop:browse_books"))
    form = ItemAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product, 
            quantity=cd['quantity'], 
            override_quantity=cd['override']
        )
    return redirect(reverse("shop:cart_detail"))


def cart_add_quick(request: HttpRequest, book_id: int) -> HttpResponse:
    cart = Cart(request)
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        if request.htmx:
            cart.add(book, 1)
            return render(request, "shop/customers/cart/partials/toast.html", {'message': "به سبد افزوده شد."})


@require_POST
def cart_remove(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)
    cart.remove(product)
    return redirect(reverse("shop:cart_detail"))


def cart_detail(request):
    cart = Cart(request)
    quantity_form = ItemAddForm()
    total = len(cart)
    count = 0
    for _ in cart:
        count += 1
    return render(request, "shop/customers/cart/detail.html", {'cart': cart, 'form': quantity_form, 'count': count, 'total': total})


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
    messages.info(request, "سبد فعلی حذف شد.")
    return redirect(reverse("shop:cart_detail"))


@role_required('user')
def get_number_of_cart_items(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    total = 0
    for i in cart:
        total += i['quantity']
    return HttpResponse(str(total))
