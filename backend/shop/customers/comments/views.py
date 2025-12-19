from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.utils import IntegrityError
from django.template.loader import render_to_string

from accounts.decorators import role_required
from shop.customers.forms import AddCommentForm
from shop.models import Book, Comment, Vote


@require_POST
@role_required('user')
def add_comment(request: HttpRequest, book_id: int) -> HttpResponse:
    book = get_object_or_404(Book, id=book_id)
    form = AddCommentForm(request.POST)
    if form.is_valid():
        try:
            Comment.objects.create(
                title = form.cleaned_data['title'],
                body = form.cleaned_data['body'],
                book = book,
                user = request.user,
                anonymous = form.cleaned_data['anonymous']
            )
        except IntegrityError as unique_error:
            return HttpResponse("شما قبلا برای این کتاب نظر ثبت کرده اید، لطفا در صورت نیاز آن را ویرایش کنید.")
        if request.htmx:
            return HttpResponse("نظر شما دریافت شد و پس از تایید نمایش داده خواهد شد.")
        messages.success(request, "نظر ثبت شد و بعد از بررسی نمایش داده خواهد شد.")
        return HttpResponseRedirect(request.path_info)
    else:
        messages.error(request, "خطایی در درج نظر رخ داد. لطفا دوباره تلاش کنید.")
        return HttpResponse(form.errors)
    

@role_required('user')
def load_book_comments(request: HttpRequest, book_id: int) -> HttpResponse:
    context = {}
    form = AddCommentForm()
    comments = Comment.objects.filter(book=book_id, status="A")
    if comments.exists():
        context['items'] = comments
        context['comment_form'] = form
    if request.htmx:
        return render(
            request, 
            "shop/customers/comments/partials/book_item_comments_partial.html", 
            context
        )
    

@role_required('user')
def upvote_comment(request: HttpRequest, comment_id: int) -> HttpResponse | JsonResponse:
    print("upvote_comment CALLED")
    if request.method == "POST":
        comment_obj = get_object_or_404(Comment, pk=comment_id)
        upvote_obj = Vote(user=request.user, comment=comment_obj, value=1)
        try:
            upvote_obj.save()
        except Exception as error:
            print(error)
            return HttpResponse("شما قبلا رای ثبت کرده اید.")
        return HttpResponse("OK")
    

@role_required('user')
def downvote_comment(request: HttpRequest, comment_id: int) -> HttpResponse | JsonResponse:
    print("downvote_comment CALLED")
    if request.method == "POST":
        comment_obj = get_object_or_404(Comment, pk=comment_id)
        downvote_obj = Vote(user=request.user, comment=comment_obj, value=-1)
        try:
            downvote_obj.save()
        except Exception as error:
            print(error)
            return HttpResponse("شما قبلا رای ثبت کرده اید.")
        return HttpResponse("OK")