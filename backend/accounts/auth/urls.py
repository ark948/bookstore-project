from django.urls import path
from accounts.auth import views

accounts_auth_endpoint_prefix = 'acc_auth_'
urlpatterns = [
    path("signup/", views.signup, name='signup'),
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
]

for endpoint in urlpatterns:
    endpoint.name = accounts_auth_endpoint_prefix + endpoint.name