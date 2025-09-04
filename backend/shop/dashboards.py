from django.shortcuts import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render
from accounts.decorators import role_required


@role_required('admin')
def admin_dashboard(request: HttpRequest) -> HttpResponse:
    return HttpResponse("دسترسی برای ادمین مجاز شناخته شد.")


@role_required('manager')
def manager_dashboard(request: HttpRequest) -> HttpResponse:
    return HttpResponse("دسترسی برای مدیر مجاز شناخته شد.")


@role_required('employee')
def employee_dashboard(request: HttpRequest) -> HttpResponse:
    return HttpResponse("دسترسی برای کارمند مجاز شناخته شد.")