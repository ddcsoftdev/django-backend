from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "description", "category"]


class ProductRestrictedSerializer(serializers.ModelSerializer):
    """Serializer that restrict all except for id, and it validates that exists"""

    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "description", "category"]

    def validate(self, attrs):
        data = self.initial_data
        extra_fields = set(data.keys()) - set(["id"])
        if extra_fields:
            raise serializers.ValidationError(
                {"product": f"Unexpected fields: {', '.join(extra_fields)}"}
            )
        product_id = data.get("id")
        if product_id:
            if not Product.objects.filter(id=product_id).exists():
                raise serializers.ValidationError(
                    {"product": "A product with this id does not exist."}
                )
        else:
            raise serializers.ValidationError({"product_id": "Required field"})

        return attrs
