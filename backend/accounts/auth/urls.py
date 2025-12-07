from django.urls import path
from accounts.auth import views

accounts_auth_endpoint_prefix = 'acc_auth_'
urlpatterns = [
    path("signup/", views.signup, name=accounts_auth_endpoint_prefix+'signup'),
    path("login/", views.login_view, name=accounts_auth_endpoint_prefix+'login'),
    path("logout/", views.logout_view, name=accounts_auth_endpoint_prefix+'logout'),
]