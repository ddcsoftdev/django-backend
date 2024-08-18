from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, logout
from .serializers import *


class UserLoginService:

    def _generate_token(self, user) -> Response:
        """Generates and saves a token for a valid user and returns Token in Response"""
        token, created = Token.objects.get_or_create(user=user)

        response = {
            "status": status.HTTP_200_OK,
            "message": "User logged in",
            "data": {"Token": token.key if token else created.key},
        }
        return Response(response, status=status.HTTP_200_OK)

    def _handle_user_token(self, request, serializer) -> Response:
        """Handles user token creation and returns Response"""
        username: str = serializer.validated_data["username"]
        password: str = serializer.validated_data["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            return self._generate_token(user=user)

        response = {
            "status": status.HTTP_401_UNAUTHORIZED,
            "error": "Credentials incorrect",
        }
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

    def handle_login(self, request) -> Response:
        """Handles login and returns Response"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return self._handle_user_token(request=request, serializer=serializer)

        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "error": "Invalid data",
            "data": serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutService:

    def _delete_token(self, serializer):
        """Tries to delete token and returns Response"""
        token = Token.objects.get(key=serializer.validated_data["token"])
        if token:
            token.delete()
            response = {"status": status.HTTP_200_OK, "message": "User logged out"}
            return Response(response, status=status.HTTP_200_OK)

        response = {"status": status.HTTP_401_UNAUTHORIZED, "error": "Token is invalid"}
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

    def handle_logout(self, request):
        """Handles logout and returns Response"""
        token_header = request.headers.get("Authorization")
        serializer = UserLogoutSerializer(data={"token": token_header})
        if serializer.is_valid():
            return self._delete_token(serializer=serializer)

        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "error": "Invalid data",
            "data": serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserSignupService:

    def handle_signup(self, request):
        """Handles signup and returns Response"""
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {"status": status.HTTP_201_CREATED, "message": "User created"}
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "error": "Invalid data",
            "data": serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
