from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('protected-page/', views.protected_view, name='prtd-page'),
]
