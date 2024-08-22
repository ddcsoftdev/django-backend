from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from eshop.utils import build_response
from .models import Order
from .serializers import OrderSerializer
from .filters import OrderFilter


def is_user_authorized(request, only_admin: bool = False) -> Response | None:
    """Checks if users is authorized for the content."""
    auth_user = request.user
    profile_data = request.data.get("user", None)
    user_data = profile_data.get("user", None) if profile_data else None

    if not auth_user.is_staff and not auth_user.is_superuser:
        if only_admin:
            return build_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message="Admin access required",
            )
        elif user_data and user_data.get("username") != auth_user.username:
            return build_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message="Access restricted to own data",
            )

    return None


class OrderListAllApi(generics.ListAPIView):
    """Lists all orders, limits non-admin/staff users to their own."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        pk = self.kwargs.get("pk")

        if not user.is_staff and not user.is_superuser:
            queryset = queryset.filter(user=user)

        if pk:
            queryset = queryset.filter(pk=pk)

        return self.filter_queryset(queryset)


class OrderCreateApi(generics.CreateAPIView):
    """Allows admin users to create a new order."""

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        error = is_user_authorized(request=request)
        if error:
            return error
        return super().post(request, *args, **kwargs)


class OrderRetrieveUpdateDestroyApi(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, or deleting a specific order."""

    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        error = is_user_authorized(request=request)
        if error:
            return error
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        error = is_user_authorized(request=request, only_admin=True)
        if error:
            return error
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        error = is_user_authorized(request=request, only_admin=True)
        if error:
            return error
        return super().delete(request, *args, **kwargs)
