from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('protected-page/', views.protected_view, name='prtd-page'),

    # CRUD actions
    path("favorite-remove/<int:book_id>/", views.remove_item_from_favorites, name='remove_favorite'),
    path("edit-comment/<int:comment_id>/", views.edit_user_comment, name='edit_comment'),
    path("delete-comment/<int:comment_id>/", views.delete_user_comment, name='delete_comment'),

    path("modify-comment/<int:comment_id>/", views.modify_comment, name='modify_comment'),

    # loaders
    path("load-orders/<str:status>", views.load_orders_with_status, name='load_orders_with_status'),
    path("load-comment-form/<int:comment_id>/", views.load_comment_form_partial, name='load_comment_form'),
    path("favorites-list/", views.favorites_list, name='fav_list'),
    path("orders-list/", views.orders_list, name='orders_list'),
    path("comments-list/", views.comments_list, name='comments_list'),

    # Profile routes
    path("profile/", views.profile, name='profile'),
    path("address/<int:profile_id>/", views.add_address, name='add_address'),
    path('ajax/load-cities/', views.load_cities, name='load_cities'),

    # Authentication routes
    path("signup/", views.signup, name='signup'),
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
]
