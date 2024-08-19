import django_filters
from .models import UserProfile


class UserProfileFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name="user__username", lookup_expr="exact"
    )
    email = django_filters.CharFilter(field_name="user__email", lookup_expr="exact")
    user_id = django_filters.NumberFilter(field_name="user__id", lookup_expr="exact")

    class Meta:
        model = UserProfile
        fields = ["username", "email", "user_id"]
