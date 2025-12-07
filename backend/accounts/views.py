from django.db.models import QuerySet
from django.shortcuts import render
from django.http import (
    HttpRequest, HttpResponse, HttpResponseForbidden
)

from accounts.models import City
from shop.models import Order

from accounts.decorators import role_required


# @login_required -> this will redirect user to login page
def protected_view(request: HttpRequest):
    if request.user.is_authenticated == False:
        return HttpResponseForbidden()
    return render(request, 'accounts/private.html')


def load_cities(request: HttpRequest) -> HttpResponse:
    province_id = request.GET.get('province')
    cities: QuerySet = City.objects.filter(province_id=province_id).order_by('name')
    return render(request, 'accounts/partials/city_dropdown_list.html', {'cities': cities})
