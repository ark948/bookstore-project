from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from icecream import ic

from accounts.decorators import role_required
from shop.customers.cart import Cart
from shop.models import (
    Book,
    Order,
    OrderItem
)


# ic| i: {'price': Decimal('300000.000'),
#         'product': <Book: shit_2>,
#         'quantity': 2,
#         'total_price': Decimal('600000.000')}
# ic| i: {'price': Decimal('150000.000'),
#         'product': <Book: کتاب دیگر_8>,
#         'quantity': 1,
#         'total_price': Decimal('150000.000')}


@role_required('user')
def checkout(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    for i in cart:
        print(i)
    total_price = 0
    for i in cart:
        total_price += i['total_price']
    total_items_count = 0
    for i in cart:
        total_items_count += i['quantity']
    items = [i for i in cart]
    if request.method == "POST":
        order_item = OrderItem.objects.create(
            total_price = total_price,
            items_count = total_items_count
        )
        for i in cart:
            order_item.books.add(i['product'])
        order_item.save()
        order = Order.objects.create(
            customer_id = request.user,
            order_items_id = order_item,
            status = Order.ORDER_STATUSES["PENDING"]
        )
        cart.clear()
        return render(request, "shop/orders/checkout.html", {'order': order})
    return render(request, "shop/orders/checkout2.html", {
        'total_price': total_price,
        'items': items,
    })


@require_POST
@role_required('user')
def fake_payment(request: HttpRequest, order_number: str) -> HttpResponse:
    order_object = get_object_or_404(Order, order_number=order_number)
    if not order_object.customer_id == request.user:
        return HttpResponseForbidden()
    if order_object.status == Order.ORDER_STATUSES['PENDING']:
        order_object.status = Order.ORDER_STATUSES['CONFIRM']
        order_object.save()
    messages.success(request, "Order payment was successful. Thank you very much.")
    # redirect to purchase placed (confirmation) page?
    return redirect(reverse('accounts:profile'))


@role_required('user')
def order_details(request: HttpRequest, order_number: str) -> HttpResponse:
    order_object = get_object_or_404(Order, order_number=order_number)
    if not order_object.customer_id == request.user:
        return HttpResponseForbidden()
    return render(request, "shop/orders/order.html", {'item': order_object})


@role_required('user')
def cancel_order(request: HttpRequest, order_number: str) -> HttpResponse:
    order_object = get_object_or_404(Order, order_number=order_number)
    if not order_object.customer_id == request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        order_object.status = Order.ORDER_STATUSES['CANCELLED']
        order_object.save()
        messages.info(request, "Order cancelled.")
        return redirect(reverse('accounts:profile'))
    return render(request, "shop/orders/cancel_order.html", {'item': order_object})


def purchase_complete(request: HttpRequest, order_id: int) -> HttpResponse:
    # get order
    # display purchase complete message
    pass