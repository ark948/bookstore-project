from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from accounts.decorators import role_required
from accounts.models import CustomUser


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "shop/customers/index.html", {})


@role_required('employee')
def customers_list(request: HttpRequest) -> HttpResponse:
    customers = CustomUser.objects.filter(role='user').order_by('email')
    if request.htmx:
        return render(request, "shop/customers/list.html", {'customers': customers})
    return render(request, "shop/customers/pages/customers_list.html", {'customers': customers})