from django.urls import path

from . import views


urlpatterns = [
    path('list/<str:status>/', views.load_comments, name='load_comments'),
    path('', views.IndexView.as_view(), name='comments_index'),
]