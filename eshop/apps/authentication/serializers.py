import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4)
    password = serializers.CharField(write_only=True, min_length=4)

    def validate_password(self, value):
        """Ensure the password contains at least one digit"""
        if not re.search(r"\d", value):
            raise ValidationError("Password must contain at least one digit")
        return value


class UserLogoutSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        """Validate the structure of the token"""
        if not value.startswith("Token "):
            raise ValidationError("Invalid token structure")
        return value.split(" ")[1]


class UserSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=4)
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def validate_username(self, value):
        """Check if the username already exists."""
        if User.objects.filter(username=value).exists():
            raise ValidationError("Username already exists")
        return value

    def validate_password(self, value):
        """Ensure the password contains at least one digit"""
        if not re.search(r"\d", value):
            raise ValidationError("Password must contain at least one digit")
        return value

    def validate_email(self, value):
        """Check if the email is valid and does not already exist"""
        email_validator = EmailValidator()
        try:
            email_validator(value)
        except ValidationError:
            raise ValidationError("Invalid email format")
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        """Hash the password before saving the new user"""
        validated_data["password"] = make_password(validated_data.get("password"))
        return super().create(validated_data)
