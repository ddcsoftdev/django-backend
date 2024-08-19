from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from eshop.utils import build_response
from .serializers import *


class CategoryDetailService:

    def handle_get(self, request) -> Response:
        category = self.get_object()  # Fetch the category using the provided PK
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_post(self, request) -> Response:
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_put(self, request) -> Response:
        category = Category.objects.all()
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_delete(self, request) -> Response:
        category = Category.objects.all()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductDetailService:

    def handle_get(self, request, pk) -> Response:
        #if pk:
        #    product = Product.objects.get(pk=pk)
        #    serializer = ProductSerializer(product)
        #else:
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

    def handle_post(self, request) -> Response:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_put(self, request) -> Response:
        product = Product.objects.all()
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_delete(self, request) -> Response:
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
