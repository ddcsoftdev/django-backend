from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .filters import CategoryFilter, ProductFilter


class CategoryListAllApi(generics.ListAPIView):
    """Lists all categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get("pk")
        if pk:
            queryset = queryset.filter(pk=pk)
        return queryset


class CategoryCreateApi(generics.CreateAPIView):
    """Allows admin users to create a new category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class CategoryRetrieveUpdateDestroyApi(generics.RetrieveUpdateDestroyAPIView):
    """Allows admin users to retrieve, update, or delete a category by its pk."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class ProductListAllApi(generics.ListAPIView):
    """Lists all products."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get("pk")
        if pk:
            queryset = queryset.filter(pk=pk)
        return queryset


class ProductCreateApi(generics.CreateAPIView):
    """Allows admin users to create a new product."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class ProductRetrieveUpdateDestroyApi(generics.RetrieveUpdateDestroyAPIView):
    """Allows admin users to retrieve, update, or delete a product by its pk."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "pk"
