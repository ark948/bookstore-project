from django.urls import path

from accounts.profile import views

urlpatterns = [
    path("favorite-remove/<int:book_id>/", views.remove_item_from_favorites, name='acc_remove_favorite'),
    path("edit-comment/<int:comment_id>/", views.edit_comment, name='acc_edit_comment'),
    path("delete-comment/<int:comment_id>/", views.delete_user_comment, name='acc_delete_comment'),
    path("favorites-list/", views.favorites_list, name='acc_fav_list'),
    path("orders-list/", views.orders_list, name='acc_orders_list'),
    path("comments-list/", views.comments_list, name='acc_comments_list'),
    path("profile/", views.profile, name='acc_profile'),
    path("address/<int:profile_id>/", views.add_address, name='acc_add_address'),
]