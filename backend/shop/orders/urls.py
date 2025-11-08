from django.urls import path

from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('fake-payment/<str:order_number>/', views.fake_payment, name='fake_payment'),
    path('order-details/<str:order_number>/', views.order_details, name='order_details'),
    path('order/cancel/<str:order_number>/', views.cancel_order, name='cancel_order'),
    path('order/invoice/download/<str:order_number>/', views.download_invoice, name='download_invoice'),

    path('orders/delete-record/<int:order_id>/', views.delete_order_record, name='delete_order_record'),
    path('orders/list/', views.orders_list, name='orders_list'),
    path('order/order-details/<int:order_id>/', views.load_order_details, name='load_order_details'),
    path('order/update-order/<int:order_id>/', views.update_order_status, name='update_order'),
]