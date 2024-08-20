from rest_framework import status
from rest_framework.response import Response
from django.http import HttpRequest
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from eshop.utils import build_response
from .serializers import UserLoginSerializer, UserLogoutSerializer, UserSignupSerializer


class UserLoginService:

    def __init__(self, request: HttpRequest):
        self.request = request
        self.serializer = UserLoginSerializer(data=request.data)

    @staticmethod
    def _generate_token(user) -> str:
        """Generates and returns a token for a valid user."""
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def _authenticate_user(self) -> Response:
        """Authenticates the user and returns the appropriate Response."""
        user = authenticate(
            self.request,
            username=self.serializer.validated_data["username"],
            password=self.serializer.validated_data["password"],
        )
        if user:
            token = self._generate_token(user)
            return build_response(
                status=status.HTTP_200_OK,
                message="User logged in",
                data={"Token": token},
            )
        return build_response(
            status=status.HTTP_401_UNAUTHORIZED, message="Credentials incorrect"
        )

    def login(self) -> Response:
        """Handles the login process and returns the appropriate Response."""
        if self.serializer.is_valid():
            return self._authenticate_user()
        return build_response(
            status=status.HTTP_400_BAD_REQUEST,
            message="Invalid data",
            data=self.serializer.data,
        )


class UserLogoutService:

    def __init__(self, request: HttpRequest):
        self.request = request
        self.token = request.headers.get("Authorization")

    @staticmethod
    def _delete_token(token_key) -> Response:
        """Deletes the token and returns the appropriate Response."""
        token = Token.objects.get(key=token_key)
        if token:
            token.delete()
            return build_response(status=status.HTTP_204_NO_CONTENT)
        return build_response(
            status=status.HTTP_404_NOT_FOUND, message="Token not found"
        )

    def logout(self) -> Response:
        """Handles the logout process and returns the appropriate Response."""
        if self.token:
            serializer = UserLogoutSerializer(data={"token": self.token})
            if serializer.is_valid():
                return self._delete_token(serializer.validated_data["token"])
        return build_response(
            status=status.HTTP_400_BAD_REQUEST,
            message="Invalid token",
            data=serializer.errors,
        )


class UserSignupService:

    def __init__(self, request: HttpRequest):
        self.serializer = UserSignupSerializer(data=request.data)

    def signup(self) -> Response:
        """Handles the signup process and returns the appropriate Response."""
        if self.serializer.is_valid():
            self.serializer.save()
            return build_response(
                status=status.HTTP_201_CREATED, message="User created"
            )
        return build_response(
            status=status.HTTP_400_BAD_REQUEST,
            message="Invalid data",
            data=self.serializer.errors,
        )
