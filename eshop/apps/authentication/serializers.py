from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ["username", "password"]


class LogoutSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ["username", "password"]


class SignupSerializer(serializers.ModelSerializer):
    """Register a new user and hash password"""

    # overriding create method to hash password
    def create(self, data):
        data["password"] = make_password(data.get("password"))
        return super(SignupSerializer, self).create(data)

    class Meta:
        model = User
        fields = ["username", "password"]
