from django.urls import path

from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('fake-payment/<str:order_number>/', views.fake_payment, name='fake_payment'),
    path('order-details/<str:order_number>/', views.order_details, name='order_details'),
    path('order/cancel/<str:order_number>/', views.cancel_order, name='cancel_order'),

    path('orders/list/', views.orders_list, name='orders_list'),
]