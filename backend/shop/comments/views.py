from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseServerError, HttpResponseBadRequest
from django.db.models import QuerySet
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.forms.models import model_to_dict

from http import HTTPStatus

from accounts.decorators import role_required
from shop.models import Comment
from . import services


class IndexView(TemplateView):
    template_name = "shop/comments/index.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated or request.user.role != "employee":
            return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        all_comments = Comment.objects.all()
        context['total'] = all_comments.count()
        context['total_waiting'] = all_comments.filter(status="Pending").count()
        context['total_rejected'] = all_comments.filter(status="Rejected").count()
        context['total_approved'] = all_comments.filter(status="Approved").count()
        return context
    

@role_required('employee')
def load_comments(request: HttpRequest, status: str) -> HttpResponse:
    comments: QuerySet = services.load_comments(status.capitalize())
    if not comments.exists():
        return HttpResponse("لیست خالی میباشد.")
    if request.htmx:
        return render(request, "shop/comments/partials/comments.html", {'comments': comments})
    return render(request, "shop/comments/pages/comments_list.html", {'comments': comments})


@require_POST
@role_required('employee')
def approve_comment(request: HttpRequest, comment_id: int) -> HttpResponse:
    # if request.headers.get("HX-Request") == "true": # to check if request is htmx without django-htmx package
    if request.htmx:
        if not services.approve_comment(comment_id):
            return HttpResponseServerError()
        return HttpResponse(status=HTTPStatus.OK)
    

@require_POST
@role_required('employee')
def reject_comment(request: HttpRequest, comment_id: int) -> HttpResponse:
    if request.htmx:
        if not services.reject_comment(comment_id):
            return HttpResponseServerError()
        return HttpResponse(status=HTTPStatus.OK)
    

def get_comment(request: HttpRequest, comment_id: int) -> HttpResponse:
    obj = get_object_or_404(Comment, pk=comment_id)
    return JsonResponse(model_to_dict(obj))


@require_POST
@role_required('user')
def vote_comment(request: HttpRequest, comment_id: int, action: str) -> HttpResponse:
    obj = get_object_or_404(Comment, pk=comment_id)
    if request.htmx:
        if action == "upvote":
            obj.positive_votes += 1
        elif action == "downvote":
            obj.negative_votes += 1
        else:
            return HttpResponseBadRequest("invalid action")
        obj.save()
        return HttpResponse(status=204)
    return redirect(reverse('shop:item_detail', kwargs={'id': obj.book.pk}))