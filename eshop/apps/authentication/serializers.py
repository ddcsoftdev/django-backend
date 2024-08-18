from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        if not value.startswith("Token "):
            raise ValidationError("Invalid token structure")
        value = value.split(" ")[1]
        return value


class SignupSerializer(serializers.ModelSerializer):

    # check if username exists
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Username already exists")
        return value

    # check if email exists
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email already exists")
        return value

    # overriding create method to hash password
    def create(self, data):
        data["password"] = make_password(data.get("password"))
        return super(SignupSerializer, self).create(data)

    class Meta:
        model = User
        fields = ["username", "password", "email"]
