from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "shop/customers/index.html", {})


def browse(request: HttpRequest) -> HttpResponse:
    return render(request, "shop/customers/browse.html", {})