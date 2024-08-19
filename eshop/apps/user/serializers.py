from rest_framework import serializers
from django.contrib.auth.models import User

from apps.authentication.serializers import UserSignupSerializer
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


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
            user_serializer = UserSignupSerializer(user, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

        return instance
