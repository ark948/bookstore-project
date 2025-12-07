from typing import Optional, Dict, Any

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import QuerySet, Q
from django.forms import model_to_dict

from accounts.models import UserProfile
from accounts.forms import UserProfileAddressForm, CommentForm
from shop.customers.forms import AddCommentForm
from shop.models import (
    Favorite,
    Order,
    Comment,
)

from accounts.decorators import role_required


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/profile/index.html")


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
            return redirect(reverse("accounts:acc_profile"))
        else:
            for field, message in form.errors.items():
                print(f"Error: {field}:, {message}")
            messages.error(request, "خطایی رخ داده است. لطفا دوباره امتحان کنید.")
            return render(request, "accounts/profile/forms/add_address.html", {'form': form})
    form = UserProfileAddressForm(instance=profile_obj)
    return render(request, "accounts/profile/forms/add_address.html", {'form': form, 'profile_obj': profile_obj})


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
        return render( request, "accounts/profile/partials/favorites.html", context)
    return render(request, "accounts/pages/favorites_list.html", context)
    

@role_required('user')
def comments_list(request: HttpRequest) -> HttpResponse:
    # time.sleep(2) to simulate server resposne delay/latency
    total_user_comments: QuerySet = Comment.objects.filter(user_id=request.user).order_by('created_at')
    approved_items = total_user_comments.filter(status="Approved")
    pending_items_count = total_user_comments.filter(status="Pending").count()
    context: Optional[Dict[str, Any]] = {}
    if total_user_comments.exists():
        context['approved_items'] = approved_items
        if approved_items.exists():
            context['approved_items_count'] = approved_items.count()
        context['pending_items_count'] = pending_items_count
        context['total'] = total_user_comments.count()
    else:
        context['total'] = 0
    if request.htmx:
        return render(request, "accounts/profile/partials/comments.html", context)
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
        return render(request, "accounts/profile/partials/orders.html", context)
    return render(request, "accounts/profile/pages/orders_list.html", context)



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
    return redirect(reverse("accounts:acc_profile"))


@role_required('user')
def edit_comment(request: HttpRequest, comment_id: int) -> HttpResponse:
    comment_obj = get_object_or_404(Comment, pk=comment_id)
    if comment_obj.user != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment_obj)
        if request.htmx:
            if form.is_valid():
                comment_obj = form.save(commit=False)
                comment_obj.status = Comment.STATUS_CHOICES['P']
                comment_obj.save()
                return HttpResponse(status=204, headers={'HX-Trigger': "edit_comment_success"})
            else:
                return render(request, "accounts/profile/forms/comment_form.html", {'form': form, 'item_id': comment_id})
        else:
            if form.is_valid():
                comment_obj = form.save(commit=False)
                comment_obj.status = Comment.STATUS_CHOICES['P']
                comment_obj.save()
                messages.success(request, "نظر با موفقیت ویرایش شد و پس از بررسی نمایش داده خواهد شد.")
                return redirect(reverse("accounts:acc_comments_list"))
            else:
                return render(request, "accounts/profile/forms/comment_form.html", {'form': form, 'item_id': comment_id})
    else:
        if request.htmx:
            form = CommentForm(instance=comment_obj)
            return render(request, "accounts/profile/forms/comment_form.html", {'form': form, 'item_id': comment_id})
        form = CommentForm(instance=comment_obj)
        return render(request, "accounts/profile/pages/forms/comment_form.html", {'form': form, 'item_id': comment_id})
    

@role_required('user')
def remove_item_from_favorites(request: HttpRequest, book_id: int) -> HttpResponse:
    if request.htmx:
        Favorite.objects.filter(user_id=request.user, book_id=book_id).delete()
        items = Favorite.objects.filter(user_id=request.user)
        context = {'items': items, 'total': items.count()}
        return render(request, "accounts/partials/favorites.html", context)


@role_required('user')
def load_comment_form_partial(request: HttpRequest, comment_id: int) -> HttpResponse:
    comment_obj = get_object_or_404(Comment, pk=comment_id)
    form = AddCommentForm(initial=model_to_dict(comment_obj))
    if request.htmx:
        if comment_obj.user != request.user:
            return HttpResponseForbidden()
        return render(
            request, 
            "accounts/forms/comment_form.html", 
            {'form': form, 'item_id': comment_id}
        )
        

@role_required('user')
def load_orders_by_status(request: HttpRequest, status: str) -> HttpResponse:
    items = Order.objects.filter(customer=request.user).filter(status=Order.ORDER_STATUSES[status])
    context = {}
    if items.exists():
        context['items'] = items
        context['total'] = items.count()
        context['status'] = status
        if request.htmx:
            return render(request, "accounts/profile/partials/orders_by_status.html", context)
    context['status'] = status
    return render(request, "accounts/profile/partials/orders_by_status.html", context)