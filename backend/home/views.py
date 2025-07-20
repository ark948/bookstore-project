from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.http import HttpResponseForbidden, HttpResponse, HttpRequest
from django.views import View
from django.utils.decorators import method_decorator

from accounts.models import CustomUser

# Create your views here.

def index(request):
    return render(request, 'home/index.html')


def has_custom_permission(user):
    # Replace with your custom logic
    return user.is_authenticated and user.is_staff

@user_passes_test(has_custom_permission, login_url='accounts//login/')
def my_view(request):
    return HttpResponse("You have access to this view!")


@user_passes_test(lambda user: user.is_authenticated, login_url='accounts:login')
def secret_view_test(request):
    return HttpResponse("Secret view.")


@permission_required('home.employee_rights')
def employee_view(request: HttpRequest):
    return HttpResponse(f"{request.user.username}, You have access to this view!")

def origin_view(request):
    if request.user and request.user.has_perm('myapp.employee_rights'):
        return HttpResponse(f"{request.user.email}, You have access to this view!")
    return HttpResponse("You do have access to this view!")


class CustomPermissionMixin:
    @method_decorator(user_passes_test(lambda user: user.is_authenticated, login_url='accounts:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

class MySecretView(CustomPermissionMixin, View):
    def get(self, request):
        return HttpResponse("Secret class-based view.")