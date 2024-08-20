import django_filters
from django.db.models import Q
from .models import Order


class OrderFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(field_name="code", lookup_expr="exact")
    purchase_date = django_filters.DateFilter(
        field_name="purchase_date", lookup_expr="exact"
    )
    username = django_filters.CharFilter(
        field_name="user__username", lookup_expr="exact"
    )
    user_email = django_filters.CharFilter(
        field_name="user__email", lookup_expr="icontains"
    )
    user_credit_card = django_filters.CharFilter(
        field_name="user__profile__credit_card", lookup_expr="icontains"
    )
    product_name = django_filters.CharFilter(
        field_name="products__name", lookup_expr="icontains"
    )
    product_category = django_filters.CharFilter(
        field_name="products__category__name", lookup_expr="icontains"
    )

    class Meta:
        model = Order
        fields = [
            "code",
            "price",
            "purchase_date",
            "username",
            "user_email",
            "user_credit_card",
            "product_name",
            "product_category",
        ]
