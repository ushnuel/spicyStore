from django.conf.urls import url
from .views import (
    add_to_cart,
    delete_from_cart,
    order_details,
    checkout,
    flutter_payment,
    update_transaction_records,
    paystack_payment,
    delete_order,
    success,
)

app_name = 'shopping_cart'

urlpatterns = [
    url(r'^add_to_cart/(?P<item_id>\d+)/$', add_to_cart, name='add_to_cart'),
    url(r'^order_summary/$', order_details, name='order_summary'),
    url(r'^checkout/$', checkout, name='checkout'),
    url(r'^item/delete/(?P<item_id>\d+)/$', delete_from_cart, name='delete_from_cart'),
    url(r'^order/delete/(?P<order_id>\d+)/$', delete_order, name='delete_order'),
    url(r'^process_payment/paystack/(?P<order_id>\d+)/$', paystack_payment, name='paystack_payment'),
    url(r'^process_payment/flutterwave/(?P<order_id>\d+)/$', flutter_payment, name='flutter_payment'),
    url(r'^update_transaction/(?P<order_id>\d+)/$', update_transaction_records, name='update_records'),
    url(r'^success/$', success, name='success'),
]
