from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.http import HttpResponse, HttpRequest
from django.views import View
from django.utils.decorators import method_decorator

from home.forms import PublicMessageForm

def index(request):
    return render(request, 'home/index.html')


def landing(request: HttpRequest) -> HttpResponse:
    return render(request, "home/landing.html")


def about(request):
    return render(request, "home/about.html")


def contact_us(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PublicMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "پیام شما ثبت شد. در صورت نیاز با شما تماس میگیریم.")
            return redirect(reverse('home:index'))
        else:
            messages.error(request, "متاسفانه خطایی در ثبت پیام رخ داده است.")
            redirect(reverse('home:contact'))
    form = PublicMessageForm()
    return render(request, "home/contact.html", {'form': form})


def has_custom_permission(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(has_custom_permission, login_url='accounts//login/')
def my_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("You have access to this view!")


@user_passes_test(lambda user: user.is_authenticated, login_url='accounts:acc_auth_login')
def secret_view_test(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Secret view.")


@permission_required('home.employee_rights')
def employee_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse(f"{request.user.username}, You have access to this view!")


def origin_view(request: HttpRequest) -> HttpResponse:
    if request.user and request.user.has_perm('myapp.employee_rights'):
        return HttpResponse(f"{request.user.email}, You have access to this view!")
    return HttpResponse("You do have access to this view!")


class CustomPermissionMixin:
    @method_decorator(user_passes_test(lambda user: user.is_authenticated, login_url='accounts:acc_auth_login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

class MySecretView(CustomPermissionMixin, View):
    def get(self, request: HttpRequest):
        return HttpResponse("Secret class-based view.")