from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('protected-page/', views.protected_view, name='prtd-page'),

    # Profile routes
    path("profile/", views.profile, name='profile'),
    path("address-2/", views.add_address_v2, name='add_address_2'),
    path("address/", views.add_address, name='add_address'),

    # Authentication routes
    path("signup/", views.signup, name='signup'),
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
]
