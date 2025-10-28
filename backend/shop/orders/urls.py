from django.urls import path

from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('fake-payment/<int:order_id>/', views.fake_payment, name='fake_payment'),
    path('order-details/<str:order_number>/', views.order_details, name='order_details'),
]