from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.contrib import messages
from icecream import ic

from . import services

from accounts.decorators import role_required
from shop.customers.cart import Cart
from shop.models import (
    Book,
    Order,
    OrderItem,
    Payment
)



@role_required('user')
def checkout(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    if len(cart) <= 0:
        messages.error(request, "سبد شما خالی میباشد.")
        return redirect(reverse('shop:customers_browse'))
    total_price = 0
    total_items_count = 0
    items = []
    for i in cart:
        total_price += i['total_price']
        total_items_count += i['quantity']
        items.append(i)
    if request.method == "POST":
        purchase_items = []
        for i in cart:
            item = OrderItem(
                book = i['product'],
                item_count = i['quantity'],
                total_price = i['product'].price * i['quantity']
            )
            item.save()
            purchase_items.append(item)
        order = Order(
            customer = request.user,
            status = Order.ORDER_STATUSES['PENDING']
        )
        order.save()
        for i in purchase_items:
            i.order = order
            i.save()
        payment = Payment.objects.create(
            customer = request.user,
            order = order,
        )
        cart.clear()
        return render(request, "shop/orders/order_placed.html", {'order': order, 'payment': payment})
    return render(request, "shop/orders/checkout.html", {
        'total_price': total_price,
        'items': items,
    })


@require_POST
@role_required('user')
def fake_payment(request: HttpRequest, order_number: str) -> HttpResponse:
    order_object = get_object_or_404(Order, order_number=order_number)
    if not order_object.customer == request.user:
        return HttpResponseForbidden()
    if order_object.status == Order.ORDER_STATUSES['PENDING']:
        order_object.status = Order.ORDER_STATUSES['CONFIRM']
        for order_item in order_object.items.all():
            book_item: Book = order_item.book
            book_item.copies_available = book_item.copies_available - order_item.item_count
            book_item.save()
        order_object.save()
    messages.success(request, "پرداخت با موفقیت انجام شد. با تشکر.")
    # redirect to purchase placed (confirmation) page?
    return redirect(reverse('accounts:profile'))


@role_required('user')
def order_details(request: HttpRequest, order_number: str) -> HttpResponse:
    order_object = get_object_or_404(Order, order_number=order_number)
    if not order_object.customer == request.user:
        return HttpResponseForbidden()
    return render(request, "shop/orders/order.html", {'item': order_object})


@role_required('user')
def cancel_order(request: HttpRequest, order_number: str) -> HttpResponse:
    order_object = get_object_or_404(Order, order_number=order_number)
    if order_object.customer != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        order_object.status = Order.ORDER_STATUSES['CANCELLED']
        order_object.save()
        payment_object = get_object_or_404(Payment, order=order_object)
        payment_object.status = Payment.PAYMENT_STATUSES[3]
        payment_object.save()
        messages.warning(request, "Order cancelled.")
        return redirect(reverse('accounts:profile'))
    return render(request, "shop/orders/cancel_order.html", {'item': order_object})


@role_required('employee')
def orders_list(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.all()
    total = orders.count()
    return render(request, "shop/orders/orders_list.html", {'items': orders, 'total': total})


@role_required('employee')
def load_order_details(request: HttpRequest, order_id: int) -> HttpResponse:
    try:
        item = Order.objects.get(pk = order_id)
        return render(request, "shop/orders/partials/order_details.html", {'item': item})
    except Order.DoesNotExist:
        return HttpResponse("404 NOT FOUND.")
    

@require_POST
@role_required('employee')
def update_order_status(request: HttpRequest, order_id: int) -> HttpResponse:
    item = get_object_or_404(Order, pk=order_id)
    new_status = request.POST.get('selected_status', None)
    if new_status:
        item.status = Order.ORDER_STATUSES[new_status]
        item.save()
    return redirect(reverse("shop:orders_list"))


@require_POST
@role_required('employee')
def delete_order_record(request: HttpRequest, order_id: int) -> HttpResponse:
    response = services.delete_order(order_id)
    if not response:
        return HttpResponseServerError()
    messages.info(request, "item removed.")
    return redirect(reverse("shop:orders_list"))