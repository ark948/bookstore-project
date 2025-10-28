from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseForbidden
from icecream import ic

from accounts.decorators import role_required
from shop.customers.cart import Cart
from shop.models import (
    Book,
    Order,
    OrderItem
)

@role_required('user')
def checkout(request: HttpRequest) -> HttpResponse:
    # cart is in session
    # get the products from cart
    # calculate the total price
    # if request is post...
    # create an order object
    # use Order.prodcuts.set() to set the products items
    # redirect to fake payment page
    # display items and their count and individual prices
    cart = Cart(request)
    items = []
    for item in cart:
        items.append(item)
    total_price = 0
    for i in items:
        print(i)
        total_price += i['price']
    if request.method == "POST":
        order_item = OrderItem.objects.create(
            total_price = total_price,
            items_count = len(items)
        )
        for i in items:
            order_item.books.add(i['product'])
        order_item.save()
        order = Order.objects.create(
            customer_id = request.user,
            order_items_id = order_item,
            status = Order.ORDER_STATUSES["PENDING"]
        )
        return render(request, "shop/orders/checkout.html", {'order': order})
    return render(request, "shop/orders/checkout.html", {
        'total_price': total_price,
        'items': items,
    })


@require_POST
@role_required('user')
def fake_payment(request: HttpRequest, order_id: int) -> HttpResponse:
    # get the order object
    # if request is post, 
    # set the is_paid of order to True
    # clear the cart
    # redirect to purchase placed page
    order_object = get_object_or_404(Order, pk=order_id)
    if not order_object.customer_id == request.user:
        return HttpResponseForbidden()
    if order_object.status == Order.ORDER_STATUSES['PENDING']:
        order_object.status = Order.ORDER_STATUSES['CONFIRM']
    return HttpResponse('ok')


@role_required('user')
def order_details(request: HttpRequest, order_number: str) -> HttpResponse:
    order_object = get_object_or_404(Order, order_number=order_number)
    if not order_object.customer_id == request.user:
        return HttpResponseForbidden()
    return render(request, "shop/orders/order.html", {'item': order_object})


def purchase_complete(request: HttpRequest, order_id: int) -> HttpResponse:
    # get order
    # display purchase complete message
    pass