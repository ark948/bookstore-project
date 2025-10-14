from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import QuerySet

from typing import Optional, Dict, Any

# Create your views here.

from .models import (
    UserProfile,
    Province,
    City
)

from shop.models import (
    Book,
    Favorite,
    Order,
    Comment,
)
from accounts.decorators import role_required
from .forms import (
    CustomUserSignUpForm,
    EmailLoginForm,
    CustomerAddressForm_widget_tweaks,
    UserProfileAddressForm
)

# signup
# login
# logout
# account recovery
# profile

def signup(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(reverse("home:index"))
    if request.method == "POST":
        form = CustomUserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/messages/signup_success.html')
    form = CustomUserSignUpForm()
    return render(request, 'accounts/forms/signup.html', {'form': form})


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(reverse("home:index"))
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username = email, password = password)
            if user != None:
                login(request, user)
                return render(request, 'accounts/messages/login_success.html')
            messages.error(request, "نام کاربری و یا رمز عبور اشتباه است.")
            return redirect(reverse("accounts:login"))
    form = EmailLoginForm()
    return render(request, 'accounts/forms/login.html', {'form': form})


@require_http_methods(['POST'])
def logout_view(request: HttpRequest):
    if request.user.is_anonymous:
        return redirect(reverse("home:index"))
    logout(request)
    return redirect(reverse("home:index"))


# @login_required -> this will redirect user to login page
def protected_view(request: HttpRequest):
    if request.user.is_authenticated == False:
        return HttpResponseForbidden()
    return render(request, 'accounts/private.html')


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/profile.html")


# add_address uses crispy_forms (this one deleted)
# add_address_v2 uses django_widget_tweaks
# to use cripsy_forms add {{ form|crispy }} to template inside the form tag
@role_required('user')
def add_address(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # form = CustomerAddressForm_widget_tweaks(request.POST)
        form = UserProfileAddressForm(request.POST)
        if form.is_valid():
            profile_obj: UserProfile = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, "آدرس با موفقیت ثبت شد.")
            return redirect(reverse("accounts:profile"))
        else:
            for field, message in form.errors.items():
                print(f"ERROR: {field} , {message}")
            messages.error(request, "خطایی رخ داده است. لطفا دوباره امتحان کنید.")
            return render(request, "accounts/forms/add_address.html", {'form': form})
    # form = CustomerAddressForm_widget_tweaks()
    form = UserProfileAddressForm()
    return render(request, "accounts/forms/add_address.html", {'form': form})


@role_required('user')
def favorites_list(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        items: QuerySet = Favorite.objects.filter(user_id=request.user).all()
        context: Optional[Dict[str, Any]] = None
        if items.exists():
            context = { 'items': items, 'total': items.count() }
        return render( request, "accounts/partials/favorites.html", context or {})
    

@role_required('user')
def comments_list(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        items: QuerySet = Comment.objects.filter(user_id=request.user).all().order_by('created_at')
        context: Optional[Dict[str, Any]] = None
        if items.exists():
            context = {
                'items': items,
                'total': items.count()
            }
        return render(request, "accounts/partials/comments.html", context or {})


@role_required('user')
def orders_list(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        items = Order.objects.filter(customer_id=request.user).all()
        if items.exists():
            return render( request, "accounts/partials/orders.html", { 'items': items } )
    return render( request, "accounts/partials/orders.html" )


@role_required('user')
def remove_favorite(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        item_id = request.GET.get('item_id')
        favorite = Favorite.objects.filter(user_id=request.user, book_id=get_object_or_404(Book, id=int(item_id)))
        if favorite:
            favorite.delete()
        items = Favorite.objects.filter(user_id=request.user).all()
        return render( request, "accounts/partials/favorites.html", { 'items': items } )
    return HttpResponse("ok")


def load_cities(request: HttpRequest) -> HttpResponse:
    province_id = request.GET.get('province')
    cities: QuerySet = City.objects.filter(province_id=province_id).order_by('name')
    return render(request, 'accounts/partials/city_dropdown_list.html', { 'cities': cities })
