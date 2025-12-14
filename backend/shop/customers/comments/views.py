from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.utils import IntegrityError
from django.template.loader import render_to_string

from accounts.decorators import role_required
from shop.customers.forms import AddCommentForm
from shop.models import Book, Comment


@require_POST
@role_required('user')
def add_comment(request: HttpRequest, book_id: int) -> HttpResponse:
    book = get_object_or_404(Book, id=book_id)
    form = AddCommentForm(request.POST)
    if form.is_valid():
        # if all data is available and no aciton is needed before saving object, use create()
        try:
            Comment.objects.create(
                title = form.cleaned_data['title'],
                body = form.cleaned_data['body'],
                book = book,
                user = request.user,
                anonymous = form.cleaned_data['anonymous']
            )
        except IntegrityError as unique_error:
            html = render_to_string('shop/customers/errors/forbidden.html', {
                'message': "شما قبلا برای این کتاب نظر ثبت کرده اید. در صورت نیاز لطفا آن را ویرایش کنید."
            })
            return HttpResponseForbidden(html)
        # return a single comment item
        # response = render(request, "shop/customers/partials/comment_item.html", {'comment': comment})
        # response['HX-Trigger'] = "comment_successfully_submitted"
        # in template, use hx-on:comment_successfully_submitted and hx-swap='beforeend' to listen to this event
        # and add the returned comment to the end of the list
        # return response
        return HttpResponse("نظر شما دریافت شد و پس از تایید نمایش داده خواهد شد.")
    else:
        # this needs to be upated with comment_form template
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