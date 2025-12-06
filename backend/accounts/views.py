from django.views.decorators.http import require_POST
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import QuerySet, Q
from django.forms import model_to_dict

from accounts.models import (
    City,
)

from accounts.forms import (
    CommentForm
)

from shop.models import (
    Favorite,
    Order,
    Comment,
)

from accounts.decorators import role_required
from shop.customers.forms import AddCommentForm


# @login_required -> this will redirect user to login page
def protected_view(request: HttpRequest):
    if request.user.is_authenticated == False:
        return HttpResponseForbidden()
    return render(request, 'accounts/private.html')


@role_required('user')
def load_orders_with_status(request: HttpRequest, status: str) -> HttpResponse:
    if request.htmx:
        items = Order.objects.filter(customer=request.user ).filter( status = Order.ORDER_STATUSES[status])
        if items.exists():
            total = items.count()
            return render(request, "accounts/partials/orders_set.html", {
                'items': items, 'total': total, 'status': status
            })
        else:
            return render(request, "accounts/partials/orders_set.html", {'status': status})


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
                return render(request, "accounts/forms/comment_form.html", {'form': form, 'item_id': comment_id})
        else:
            if form.is_valid():
                comment_obj = form.save(commit=False)
                comment_obj.status = Comment.STATUS_CHOICES['P']
                comment_obj.save()
                messages.success(request, "نظر با موفقیت ویرایش شد و پس از بررسی نمایش داده خواهد شد.")
                return redirect(reverse("accounts:acc_comments_list"))
            else:
                return render(request, "accounts/forms/comment_form.html", {'form': form, 'item_id': comment_id})
    else:
        if request.htmx:
            form = CommentForm(instance=comment_obj)
            return render(request, "accounts/forms/comment_form.html", {'form': form, 'item_id': comment_id})
        form = CommentForm(instance=comment_obj)
        return render(request, "accounts/pages/forms/comment_form.html", {'form': form, 'item_id': comment_id})
        

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


def load_cities(request: HttpRequest) -> HttpResponse:
    province_id = request.GET.get('province')
    cities: QuerySet = City.objects.filter(province_id=province_id).order_by('name')
    return render(request, 'accounts/partials/city_dropdown_list.html', {'cities': cities})
