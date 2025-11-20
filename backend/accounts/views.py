from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import QuerySet, Q
from django.forms import model_to_dict

from typing import Optional, Dict, Any

# Create your views here.

from .models import (
    UserProfile,
    City,
)

from shop.models import (
    Favorite,
    Order,
    Comment,
)
from accounts.decorators import role_required
from .forms import (
    CustomUserSignUpForm,
    EmailLoginForm,
    UserProfileAddressForm
)

from shop.customers.forms import AddCommentForm

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


@role_required('user')
def add_address(request: HttpRequest, profile_id: int) -> HttpResponse:
    profile_obj = UserProfile.objects.get(pk=profile_id)
    if request.method == "POST":
        form = UserProfileAddressForm(request.POST, instance=profile_obj)
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
    form = UserProfileAddressForm(instance=profile_obj)
    return render(request, "accounts/forms/add_address.html", {'form': form, 'profile_obj': profile_obj})


@role_required('user')
def favorites_list(request: HttpRequest) -> HttpResponse:
    items: QuerySet = Favorite.objects.filter(user_id=request.user)
    context: Optional[Dict[str, Any]] = {}
    if items.exists():
        context['items'] = items
        context['total'] = items.count()
    else:
        context['total'] = 0
    if request.htmx:
        return render( request, "accounts/partials/favorites.html", context)
    return render(request, "accounts/pages/favorites_list.html", context)
    

@role_required('user')
def comments_list(request: HttpRequest) -> HttpResponse:
    # time.sleep(2) to simulate server resposne delay/latency
    items: QuerySet = Comment.objects.filter(user_id=request.user, status="Approved").order_by('created_at')
    context: Optional[Dict[str, Any]] = {}
    if items.exists():
        context['items'] = items
        context['total'] = items.count()
    else:
        context['total'] = 0
    if request.htmx:
        return render(request, "accounts/partials/comments.html", context)
    return render(request, "accounts/pages/comments_list.html", context)


@role_required('user')
def orders_list(request: HttpRequest) -> HttpResponse:
    items = Order.objects.filter(customer=request.user)
    context = {}
    if items.exists():
        total = items.count()
        total_active = items.filter(
            Q(status=Order.ORDER_STATUSES['PENDING']) | Q(status=Order.ORDER_STATUSES['CONFIRM'])
        ).count()
        context['items'] = items
        context['total'] = total
        context['total_active'] = total_active
    else:
        context['total'] = 0
    if request.htmx:
        return render(request, "accounts/partials/orders.html", context)
    return render(request, "accounts/pages/orders_list.html", context)


@role_required('user')
def load_orders_with_status(request: HttpRequest, status: str) -> HttpResponse:
    if request.htmx:
        items = Order.objects.filter( customer=request.user ).filter( status = Order.ORDER_STATUSES[status] )
        if items.exists():
            total = items.count()
            return render(request, "accounts/partials/orders_set.html", {
                'items': items,
                'total': total,
                'status': status
            })
        else:
            return render(request, "accounts/partials/orders_set.html", { 'status': status })


@role_required('user')
def remove_item_from_favorites(request: HttpRequest, book_id: int) -> HttpResponse:
    if request.htmx:
        Favorite.objects.filter( user_id=request.user, book_id=book_id ).delete()
        items = Favorite.objects.filter( user_id=request.user )
        context = { 'items': items, 'total': items.count() }
        return render(request, "accounts/partials/favorites.html", context)


@role_required('user')
def load_comment_form_partial(request: HttpRequest, comment_id: int) -> HttpResponse:
    comment_obj = get_object_or_404(Comment, pk=comment_id)
    form = AddCommentForm(initial=model_to_dict(comment_obj))
    if request.htmx:
        if comment_obj.user != request.user:
            return HttpResponseForbidden()
        return render(request, "accounts/forms/comment_form.html", {'form': form, 'item_id': comment_id})


@require_POST
@role_required('user')
def edit_user_comment(request: HttpRequest, comment_id: int) -> HttpResponse:
    comment_obj = get_object_or_404(Comment, pk=comment_id)
    if request.htmx:
        if comment_obj.user != request.user:
            return HttpResponseForbidden()
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment_obj.body = form.cleaned_data['body']
            comment_obj.title = form.cleaned_data['title']
            comment_obj.status = "Pending"
            comment_obj.save()
            response = HttpResponse()
            response['HX-Trigger'] = "edit_comment_success"
            return response
        else:
            return HttpResponse("ERROR", status=422)
        

@require_POST
@role_required('user')
def delete_user_comment(request: HttpRequest, comment_id: int) -> HttpResponse:
    comment_obj = get_object_or_404(Comment, pk=comment_id)
    if request.htmx:
        if comment_obj.user != request.user:
            return HttpResponseForbidden()
        comment_obj.delete()
        return HttpResponse("نظر حذف شد.")
    messages.error(request, "خطایی رخ داده است.")
    return redirect(reverse("accounts:profile"))


def load_cities(request: HttpRequest) -> HttpResponse:
    province_id = request.GET.get('province')
    cities: QuerySet = City.objects.filter(province_id=province_id).order_by('name')
    return render(request, 'accounts/partials/city_dropdown_list.html', { 'cities': cities })
