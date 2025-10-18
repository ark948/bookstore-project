from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import QuerySet
from django.views.generic import TemplateView

from accounts.decorators import role_required
from accounts.models import CustomUser, UserProfile
from shop.models import Comment, Book


class IndexView(TemplateView):
    template_name = "shop/comments/index.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        all_comments = Comment.objects.all()
        context['total'] = all_comments.count()
        context['total_waiting'] = all_comments.filter(status="Pending").count()
        context['total_rejected'] = all_comments.filter(status="Rejected").count()
        context['total_approved'] = all_comments.filter(status="Approved").count()
        return context