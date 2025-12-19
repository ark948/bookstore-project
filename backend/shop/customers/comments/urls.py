from django.urls import path

from shop.customers.comments import views

urlpatterns = [
    path("downvote-comment/<int:comment_id>/", views.downvote_comment, name='downvote_comment'),
    path("upvote-comment/<int:comment_id>/", views.upvote_comment, name='upvote_comment'),
    path("add-comment/<int:book_id>/", views.add_comment, name='add_comment'),
    path("load-book-comments/<int:book_id>/", views.load_book_comments, name='load_book_comments'),
]