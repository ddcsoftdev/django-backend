from rest_framework import serializers
from django.contrib.auth.models import User
from apps.authentication.serializers import UserSignupSerializer
from django.contrib.auth.hashers import make_password
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    # non required for update
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "first_name", "last_name"]


class UserProfileSerializer(serializers.ModelSerializer):
    # not required if only profile data is updated
    user = UserSerializer(required=False)

    class Meta:
        model = UserProfile
        fields = ["user", "credit_card", "address", "mobile"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        user = instance.user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if user_data:
            if "password" in user_data:
                user_data["password"] = make_password(user_data["password"])
            user_serializer = UserSignupSerializer(user, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

        return instance


class UserProfileRestrictedSerializer(serializers.ModelSerializer):
    """Restricts all fields except user.username, which validates if is in database."""

    user = UserSerializer(required=True)

    class Meta:
        model = UserProfile
        fields = ["user", "credit_card", "address", "mobile"]

    def _check_extra_fields(self, data: dict) -> dict:
        """Validates that no extra fields are used, return User data"""
        # check UserProfile
        extra_fields = set(data.keys()) - set(["user"])
        if extra_fields:
            raise serializers.ValidationError(
                {"user": f"Unexpected fields: {', '.join(extra_fields)}"}
            )
        # check User
        user_data = data.get("user", None)
        extra_fields = set(user_data.keys()) - set(["username"])
        if extra_fields:
            raise serializers.ValidationError(
                {"detail": f"Unexpected fields: {', '.join(extra_fields)}"}
            )
        return user_data

    def _check_username_exists(self, data: dict):
        """Validates that username exists in database"""
        username = data.get("username")
        if username:
            if not User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    {"username": "A user with this username does not exist."}
                )
        else:
            raise serializers.ValidationError({"username": "Required field"})

    def validate(self, attrs):
        user_data: dict = self._check_extra_fields(data=attrs)
        self._check_username_exists(data=user_data)
        return attrs
