from django.urls import path

from accounts.profile import views

urlpatterns = [
    path("favorites-list/", views.favorites_list, name='acc_fav_list'),
    path("orders-list/", views.orders_list, name='acc_orders_list'),
    path("comments-list/", views.comments_list, name='acc_comments_list'),
    path("profile/", views.profile, name='acc_profile'),
    path("address/<int:profile_id>/", views.add_address, name='acc_add_address'),
]