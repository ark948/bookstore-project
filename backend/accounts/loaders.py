from django.db.models import QuerySet
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from accounts.models import City

def load_cities(request: HttpRequest) -> HttpResponse:
    province_id = request.GET.get('province')
    cities: QuerySet = City.objects.filter(province_id=province_id).order_by('name')
    return render(request, 'accounts/loaders/city_dropdown_list.html', {'cities': cities})