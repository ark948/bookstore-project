from django.urls import path

from . import views


urlpatterns = [
    path('reject-comment/<int:comment_id>/', views.reject_comment, name='reject_comment'),
    path('approve-comment/<int:comment_id>/', views.approve_comment, name='approve_comment'),
    path('list/<str:status>/', views.load_comments, name='load_comments'),
    path('list/non-js/<str:status>/', views.load_comments, name='comments_list'),
    path('', views.IndexView.as_view(), name='comments_index'),
]