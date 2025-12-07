from django.urls import path, include

from accounts import views

accounts_endpoints_prefix = 'acc'
app_name = 'accounts'
urlpatterns = [
    # loaders
    path('ajax/load-cities/', views.load_cities, name='acc_load_cities'),

    # Profile routes
    path('profile/', include('accounts.profile.urls')),

    # Authentication routes
    path('auth/', include('accounts.auth.urls')),

    path('protected-page/', views.protected_view, name='acc_prtd_page'),
]