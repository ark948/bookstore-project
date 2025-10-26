from django.shortcuts import render, redirect, get_object_or_404
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from accounts.decorators import role_required

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
    pass


def fake_payment(request: HttpRequest, order_id: int) -> HttpResponse:
    # get the order object
    # if request is post, 
    # set the is_paid of order to True
    # clear the cart
    # redirect to purchase placed page
    pass


def purchase_complete(request: HttpRequest, order_id: int) -> HttpResponse:
    # get order
    # display purchase complete message
    pass