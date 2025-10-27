from django.urls import path

from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('fake-payment/<int:order_id>/', views.fake_payment, name='fake_payment'),
]