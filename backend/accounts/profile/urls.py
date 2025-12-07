from django.urls import path

from accounts.profile import views

accounts_profile_endpoint_prefix = 'acc_prf_'
urlpatterns = [
    path("favorite-remove/<int:book_id>/", views.remove_item_from_favorites, name=accounts_profile_endpoint_prefix+'remove_favorite'),
    path("edit-comment/<int:comment_id>/", views.edit_comment, name=accounts_profile_endpoint_prefix+'edit_comment'),
    path("delete-comment/<int:comment_id>/", views.delete_user_comment, name=accounts_profile_endpoint_prefix+'delete_comment'),
    path("favorites-list/", views.favorites_list, name=accounts_profile_endpoint_prefix+'favorites_list'),
    path("orders-list/", views.orders_list, name=accounts_profile_endpoint_prefix+'orders_list'),
    path("comments-list/", views.comments_list, name=accounts_profile_endpoint_prefix+'comments_list'),
    path("load-comment-form/<int:comment_id>/", views.load_comment_form_partial, name=accounts_profile_endpoint_prefix+'load_comment_form'),
    path("load-orders/<str:status>", views.load_orders_by_status, name=accounts_profile_endpoint_prefix+'load_orders_with_status'),
    path("profile/", views.profile, name=accounts_profile_endpoint_prefix+'profile'),
    path("address/<int:profile_id>/", views.add_address, name=accounts_profile_endpoint_prefix+'add_address'),
]