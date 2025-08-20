from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST

from shop.models import Book
from .cart import Cart
from .forms import ItemAddForm


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "shop/customers/index.html", {})


def browse(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    return render(request, "shop/customers/browse.html", {"items": books})


@require_POST
def cart_add(request: HttpRequest, product_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)
    form = ItemAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect(reverse("shop:cart-details"))


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)
    cart.remove(product)
    return redirect(reverse("shop:cart-details"))


def cart_detail(request):
    cart = Cart(request)
    return render(request, "shop/customers/cart.html", {'cart': cart})