from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    class Meta:
        model = Category
        fields = ["id", "name"]


class CategoryRestrictedSerializer(serializers.ModelSerializer):
    """Serializer for restricted category operations, allowing only id and name fields."""
    
    name = serializers.CharField(required=False)

    class Meta:
        model = Category
        fields = ["id", "name"]

    def validate(self, attrs):
        """Validate input data, ensuring no extra fields are provided."""
        data = self.initial_data
        extra_fields = set(data.keys()) - {"id"}
        if extra_fields:
            raise serializers.ValidationError(
                {"category": f"Unexpected fields: {', '.join(extra_fields)}"}
            )

        category_id = data.get("id")
        if not category_id:
            raise serializers.ValidationError({"category_id": "Required field"})

        if not Category.objects.filter(id=category_id).exists():
            raise serializers.ValidationError(
                {"category": "A category with this ID does not exist."}
            )

        return attrs


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model, with category details included."""
    
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "description", "category"]

    def _get_category(self):
        """Validate and return the category, None or flag to delete"""
        category_data = self.initial_data.get("category")
        if not category_data:
            return None
        elif category_data["id"] == -1:
            return -1

        serializer = CategoryRestrictedSerializer(data=category_data)
        serializer.is_valid(raise_exception=True)
        return Category.objects.get(id=category_data["id"])

    def create(self, validated_data):
        category = self._get_category()    
        product = Product.objects.create(category=category, **validated_data)
        return product

    def update(self, instance, validated_data):
        category = self._get_category()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if category == -1:
            instance.category = None
        elif category:
            instance.category = category

        instance.save()
        return instance


class ProductRestrictedSerializer(serializers.ModelSerializer):
    """Serializer that restricts all fields except id."""
    
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "description", "category"]

    def validate(self, attrs):
        data = self.initial_data
        extra_fields = set(data.keys()) - {"id"}
        if extra_fields:
            raise serializers.ValidationError(
                {"product": f"Unexpected fields: {', '.join(extra_fields)}"}
            )

        product_id = data.get("id")
        if not product_id:
            raise serializers.ValidationError({"product_id": "Required field"})

        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError(
                {"product": "A product with this ID does not exist."}
            )

        return attrs
