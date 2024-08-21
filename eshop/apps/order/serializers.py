from rest_framework import serializers
from apps.product.serializers import ProductSerializer, ProductRestrictedSerializer
from apps.user.serializers import UserProfileSerializer, UserProfileRestrictedSerializer
from apps.user.models import User
from apps.product.models import Product
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True)
    user = UserProfileSerializer(source="user.profile", read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "code",
            "price",
            "purchase_date",
            "user",
            "products",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.get("request").method == "PUT":
            self._make_fields_optional(["code", "price", "purchase_date"])

    def _make_fields_optional(self, fields):
        """Set specified fields as not required."""
        for field in fields:
            self.fields[field].required = False

    def _get_products(self) -> list:
        """Validate and return the list of products."""
        products_data = self.initial_data.get("products")
        if not products_data:
            raise serializers.ValidationError(
                {"products": "At least one product is required"}
            )

        products: list = []
        for product in products_data:
            serializer = ProductRestrictedSerializer(data=product)
            serializer.is_valid(raise_exception=True)
            product_instance = Product.objects.get(pk=product["id"])
            products.append(product_instance)
        return products

    def _get_user(self):
        """Validate and return the user."""
        user_data = self.initial_data.get("user")
        if not user_data:
            raise serializers.ValidationError({"user": "User is missing"})

        serializer = UserProfileRestrictedSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        return User.objects.get(username=user_data["user"]["username"])

    def create(self, validated_data):
        products = self._get_products()
        user = self._get_user()
        order = Order.objects.create(user=user, **validated_data)
        order.products.set(products)
        return order

    def update(self, instance, validated_data):
        products = self._get_products()
        user = self._get_user()

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.user = user
        instance.save()
        instance.products.set(products)
        return instance
