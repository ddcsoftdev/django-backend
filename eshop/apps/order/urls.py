from django.urls import re_path
from .views import *

#urls
orders_url = r"^orders/?$"
orders_url_pk = r"^orders/(?P<pk>\d+)/?$"
order_url = r"^order/?$"
order_url_pk = r"^order/(?P<pk>\d+)/?$"

urlpatterns = [
    re_path(orders_url, OrderListAllApi().as_view(), name="orders"),
    re_path(orders_url_pk, OrderListAllApi().as_view(), name="orders-pk"),
    re_path(order_url, OrderCreateApi().as_view(), name="order"),
    re_path(order_url_pk, OrderRetrieveUpdateDestroyApi().as_view(), name="order-pk"),
]