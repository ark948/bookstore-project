from django.urls import path

from . import views


urlpatterns = [
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('approve-comment/<int:comment_id>/', views.approve_comment, name='approve_comment'),
    path('list/<str:status>/', views.load_comments, name='load_comments'),
    path('', views.IndexView.as_view(), name='comments_index'),
]