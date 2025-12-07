from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import render
from django.urls import path, include

from accounts import loaders


# @login_required -> this will redirect user to login page
def protected_view(request: HttpRequest):
    if request.user.is_authenticated == False:
        return HttpResponseForbidden()
    return render(request, 'accounts/private.html')


accounts_endpoints_prefix = 'acc_'
app_name = 'accounts'
urlpatterns = [
    path('ajax/load-cities/', loaders.load_cities, name=accounts_endpoints_prefix+'load_cities'),
    path('protected-page/', protected_view, name=accounts_endpoints_prefix+'prtd_page'),
    
    path('profile/', include('accounts.profile.urls')),
    path('auth/', include('accounts.auth.urls')),
]