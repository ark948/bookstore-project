from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [

    path('set-address/', views.address_form_view, name='address_form'),
    path('ajax/load-cities/', views.load_cities, name='load_cities'),

    path('protected-page/', views.protected_view, name='prtd-page'),

    path("favorite-remove/", views.remove_favorite, name='remove_favorite'),

    # loaders
    path("favorites-list/", views.favorites_list, name='fav_list'),
    path("orders-list/", views.orders_list, name='orders_list'),

    # Profile routes
    path("profile/", views.profile, name='profile'),
    path("address/", views.add_address, name='add_address'),

    # Authentication routes
    path("signup/", views.signup, name='signup'),
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
]
