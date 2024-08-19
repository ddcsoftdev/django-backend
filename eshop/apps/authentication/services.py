from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserLoginSerializer, UserLogoutSerializer, UserSignupSerializer


def build_response(status_code, message=None, data=None) -> Response:
    """Builds and returns a standard response format"""
    response_data = {"status": status_code}

    if message:
        response_data["message"] = message
    if data:
        response_data["data"] = data

    return Response(response_data, status=status_code)


class UserLoginService:

    @staticmethod
    def _generate_token(user) -> str:
        """Generates and returns a token for a valid user"""
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def _authenticate_user(self, request, serializer) -> Response:
        """Authenticates the user and returns the appropriate Response"""
        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user:
            token = self._generate_token(user)
            return build_response(
                status.HTTP_200_OK, "User logged in", {"Token": token}
            )

        return build_response(status.HTTP_401_UNAUTHORIZED, "Credentials incorrect")

    def handle_login(self, request) -> Response:
        """Handles the login process and returns the appropriate Response"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return self._authenticate_user(request, serializer)
        return build_response(
            status.HTTP_400_BAD_REQUEST, "Invalid data", serializer.errors
        )


class UserLogoutService:

    @staticmethod
    def _delete_token(token_key) -> Response:
        """Deletes the token and returns the appropriate Response"""
        try:
            token = Token.objects.get(key=token_key)
            token.delete()
            return build_response(status.HTTP_200_OK, "User logged out")
        except Token.DoesNotExist:
            return build_response(status.HTTP_401_UNAUTHORIZED, "Token is invalid")

    def handle_logout(self, request) -> Response:
        """Handles the logout process and returns the appropriate Response"""
        token_key = request.headers.get("Authorization")
        if not token_key:
            return build_response(
                status.HTTP_400_BAD_REQUEST, "Authorization header is missing"
            )
        serializer = UserLogoutSerializer(data={"token": token_key})
        if serializer.is_valid():
            return self._delete_token(serializer.validated_data["token"])
        return build_response(
            status.HTTP_400_BAD_REQUEST, "Invalid data", serializer.errors
        )


class UserSignupService:
    @staticmethod
    def handle_signup(request) -> Response:
        """Handles the signup process and returns the appropriate Response"""
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return build_response(status.HTTP_201_CREATED, "User created")
        return build_response(
            status.HTTP_400_BAD_REQUEST, "Invalid data", serializer.errors
        )
