from django.urls import path, include

from accounts import views

accounts_endpoints_prefix = 'acc' # this must be applied to all endpoints in this app except the very specific ones
app_name = 'accounts'
urlpatterns = [
    # CRUD actions
    path("favorite-remove/<int:book_id>/", views.remove_item_from_favorites, name='acc_remove_favorite'),
    path("edit-comment/<int:comment_id>/", views.edit_comment, name='acc_edit_comment'),
    path("delete-comment/<int:comment_id>/", views.delete_user_comment, name='acc_delete_comment'),

    # loaders
    path("load-orders/<str:status>", views.load_orders_with_status, name='acc_load_orders_with_status'),
    path("load-comment-form/<int:comment_id>/", views.load_comment_form_partial, name='acc_load_comment_form'),

    path('ajax/load-cities/', views.load_cities, name='acc_load_cities'),

    # Profile routes
    path('profile/', include('accounts.profile.urls')),

    # Authentication routes
    path('auth/', include('accounts.auth.urls')),

    path('protected-page/', views.protected_view, name='acc_prtd_page'),
]