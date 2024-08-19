import django_filters
from .models import Category, Product


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="iexact")

    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="iexact")
    category = django_filters.CharFilter(
        field_name="category__name", lookup_expr="iexact"
    )

    class Meta:
        model = Product
        fields = ["id", "name", "category"]
