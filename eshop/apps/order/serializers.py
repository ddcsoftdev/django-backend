from rest_framework import serializers
from apps.product.serializers import ProductSerializer
from apps.user.serializers import UserSerializer, UserProfileSerializer
from apps.user.models import UserProfile
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False)
    user = UserProfileSerializer(source='user.profile', read_only=True)
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
