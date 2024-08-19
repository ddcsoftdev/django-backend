from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAdminUser,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from rest_framework import status
from .serializers import CategorySerializer, ProductSerializer
from .filters import CategoryFilter, ProductFilter
from .services import *


class CategoryListAllApi(generics.ListAPIView):
    """Lists all categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter


class CategoryDetailApi(APIView):
    """Allows to create, modify or delete categories"""

    permission_classes = [IsAuthenticatedOrReadOnly]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category_service = CategoryDetailService()

    def check_permissions(self, request):
        """Set admin permission for POST PUT and DELETE"""
        if request.method in ["POST", "PUT", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        super().check_permissions(request)

    def get(self, request, pk=None) -> Response:
        """Retrieve a category or list of categories."""
        return self._handle_request(self.category_service.handle_get, request)

    def post(self, request) -> Response:
        """Create a new category."""
        return self._handle_request(self.category_service.handle_post, request)

    def put(self, request) -> Response:
        """Update an existing category."""
        return self._handle_request(self.category_service.handle_put, request)

    def delete(self, request) -> Response:
        """Delete an existing category."""
        return self._handle_request(self.category_service.handle_delete, request)

    def _handle_request(self, service_method, request) -> Response:
        """Handles exceptions for the service methods."""
        try:
            return service_method(request=request)
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class ProductListAllApi(generics.ListAPIView):
    """Lists all products."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class ProdcutsDetailApi(APIView):
    """Allows to create, modify or delete products"""

    permission_classes = [IsAuthenticatedOrReadOnly]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductDetailService()

    def check_permissions(self, request):
        """Set admin permission for POST PUT and DELETE"""
        if request.method in ["POST", "PUT", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        super().check_permissions(request)

    def get(self, request, pk=None):
        """Retrieve a category or list of categories."""
        return self._handle_request(self.product_service.handle_get, request)

    def post(self, request):
        """Create a new category."""
        return self._handle_request(self.product_service.handle_post, request)

    def put(self, request, pk):
        """Update an existing category."""
        return self._handle_request(self.product_service.handle_put, request)

    def delete(self, request, pk):
        """Delete an existing category."""
        return self._handle_request(self.product_service.handle_delete, request)

    def _handle_request(self, service_method, request) -> Response:
        """Handles exceptions for the service methods."""
        try:
            return service_method(request=request)
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)
