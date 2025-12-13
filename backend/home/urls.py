from django.urls import path

from home import views

app_name = 'home'
urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact-us/', views.contact_us, name='contact'),
    path('', views.landing, name='index'),

    # routes for development and testing
    path('secret/', views.secret_view_test, name='secret_1'),
    path('secret-2/', views.MySecretView.as_view(), name='secret_2'),
]