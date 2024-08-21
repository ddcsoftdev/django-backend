from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from apps.user.models import User
from rest_framework.response import Response
from apps.product.models import Product
from eshop.utils import handle_request, is_user_authorized
from .models import Order
from .serializers import OrderSerializer
from apps.user.serializers import UserProfileRestrictedSerializer
from apps.product.serializers import ProductRestrictedSerializer
from .filters import OrderFilter


class OrderListAllApi(generics.ListAPIView):
    """Lists all orders, limits non admin/staff to their own."""

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
            return queryset.filter(pk=pk)
        filter_backend = DjangoFilterBackend()
        queryset = filter_backend.filter_queryset(self.request, queryset, self)
        return queryset

    
class OrderCreateApi(generics.CreateAPIView):
    """Allows admin users to create a new order."""

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    def post(self, request, *args, **kwargs):
        error = is_user_authorized(request=request)
        if error is not None:
            return error
        return super().post(request, *args, **kwargs)


class OrderRetrieveUpdateDestroyApi(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get(self, request, *args, **kwargs):
        error = is_user_authorized(request=request)
        if error is not None:
            return error    
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        error = is_user_authorized(request=request, only_admin=True)
        if error is not None:
            return error 
        return super().put(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        error = is_user_authorized(request=request, only_admin=True)
        if error is not None:
            return error 
        return super().delete(request, *args, **kwargs)