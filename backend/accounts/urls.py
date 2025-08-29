from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('submit-address/', views.add_address, name='add_address'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('protected-page/', views.protected_view, name='prtd-page'),
    path("profile/", views.profile, name='profile'),
]
