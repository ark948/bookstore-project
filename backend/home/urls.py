from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('secret/', views.secret_view_test, name='secret-1'),
    path('secret-2/', views.MySecretView.as_view(), name='secret-2'),
    path('', views.index, name='index'),
]