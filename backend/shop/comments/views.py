from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseServerError
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import QuerySet
from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods, require_POST

from http import HTTPStatus

from accounts.decorators import role_required
from accounts.models import CustomUser, UserProfile
from shop.models import Comment, Book
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
    return render(request, "shop/comments/partials/comments.html", {'comments': comments})


@require_POST
@role_required('employee')
def approve_comment(request: HttpRequest, comment_id: int) -> HttpResponse:
    # if request.headers.get("HX-Request") == "true": # to check if request is htmx without django-htmx package
    if request.htmx:
        if not services.update_comment(comment_id, 'A'):
            return HttpResponseServerError()
        return HttpResponse(status=HTTPStatus.OK)
    

@require_POST
@role_required('employee')
def reject_comment(request: HttpRequest, comment_id: int) -> HttpResponse:
    if request.htmx:
        if not services.update_comment(comment_id, 'R'):
            return HttpResponseServerError()
        return HttpResponse(status=HTTPStatus.OK)


@role_required('employee')
def delete_comment(request: HttpRequest, comment_id: int) -> HttpResponse:
    if request.htmx:
        if not services.remove_comment(comment_id):
            return HttpResponseServerError()
        return HttpResponse(status=HTTPStatus.OK)