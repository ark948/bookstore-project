from typing import Dict, List, Optional, Required, Any, Tuple
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from shop.models import Order


def update_order_status(value: Any, order_id: Optional[int] = None, 
            order_number: Optional[str] = None
        ) -> dict:
    if not (order_id or order_number):
        raise ValueError("Either order_id or order_number is required.")
    if order_id:
        order_obj = get_object_or_404(Order, pk=order_id)
    elif order_number:
        order_obj = get_object_or_404(Order, order_number=order_number)
    order_obj.status = Order.ORDER_STATUSES[value]
    try:
        order_obj.save()
    except Exception as error:
        return {
            'status': 'failure',
            'message': error
        }
    return order_obj


def delete_order( order_id: int ) -> Tuple | bool:
    item = Order.objects.get(pk=order_id)
    if item:
        try:
            response = item.delete()
            return response
        except Exception as error:
            print(error)
            return False
    