from rest_framework import serializers
from apps.product.serializers import ProductSerializer
from apps.user.serializers import UserProfileSerializer, UserProfileRestrictedSerializer
from apps.product.serializers import ProductRestrictedSerializer
from django.forms.models import model_to_dict
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
            self.fields["code"].required = False
            self.fields["price"].required = False
            self.fields["purchase_date"].required = False

    def get_products(self, data) -> list:
        data = self.initial_data.get("products", None)
        if data is None:
            raise serializers.ValidationError(
                {"product": "At least one product required"}
            )
        products: list = []
        for product in data:
            serializer = ProductRestrictedSerializer(data=product)
            if serializer.is_valid(raise_exception=True):
                product = Product.objects.get(pk=product["id"])
                products.append(product)
        return products

    def get_user(self, data):
        user = self.initial_data.get("user", None)
        if data is None:
            raise serializers.ValidationError({"user": "User missing"})
        serializer = UserProfileRestrictedSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(username=user["user"]["username"])
        return user

    def create(self, validated_data):
        products = self.get_products(data=self.initial_data)
        user = self.get_user(data=self.initial_data)
        order = Order.objects.create(user=user, **validated_data)
        order.products.set(products)
        return order

    def update(self, instance, validated_data):
        products = self.get_products(data=self.initial_data)
        user = self.get_user(data=self.initial_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user = user
        instance.save()
        instance.products.set(products)
        return instance
