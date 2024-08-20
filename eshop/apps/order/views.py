from rest_framework import generics
from rest_framework.permissions import IsAuthenticated , AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from apps.user.models import User
from .models import Order
from .serializers import OrderSerializer
from .filters import OrderFilter


class OrderListAllApi(generics.ListAPIView):
    """Lists all orders, limits non admin/staff to their own."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_staff and not user.is_superuser:
            queryset = queryset.filter(user=user)

        filter_backend = DjangoFilterBackend()
        queryset = filter_backend.filter_queryset(self.request, queryset, self)

        pk = self.kwargs.get("pk")
        if pk:
            queryset = queryset.filter(pk=pk)
        return queryset


class OrderCreateApi(generics.CreateAPIView):
    """Allows admin users to create a new order."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_staff and not user.is_superuser:
            serializer.save(user=user)
       
        profile = self.request.data.get("user").get("user")
        if profile:
            user = User.objects.get(username=profile["username"])
        serializer.save(user=user)


class OrderRetrieveUpdateDestroyApi(generics.RetrieveUpdateDestroyAPIView):
    """Allows retrive, update, or delete an order by its pk."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_staff and not user.is_superuser:
            queryset = queryset.filter(user=user)
        return queryset

    def perform_update(self, serializer):
        user = self.request.user
        if not user.is_staff and not user.is_superuser:
            serializer.save(user=user)
        else:
            serializer.save()
