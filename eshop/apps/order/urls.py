from django.urls import re_path
from django.conf import settings
from .views import *

#urls
orders_url = r"^" + settings.API_URL + r"orders/?$"
orders_url_pk = r"^" + settings.API_URL + r"orders/(?P<pk>\d+)/?$"
order_url = r"^" + settings.API_URL + r"order/?$"
order_url_pk = r"^" + settings.API_URL + r"order/(?P<pk>\d+)/?$"

urlpatterns = [
    re_path(orders_url, OrderListAllApi().as_view(), name="orders"),
    re_path(orders_url_pk, OrderListAllApi().as_view(), name="orders"),
    re_path(order_url, OrderCreateApi().as_view(), name="order"),
    re_path(order_url_pk, OrderRetrieveUpdateDestroyApi().as_view(), name="order"),
]