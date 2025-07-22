from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "customers/index.html", {})