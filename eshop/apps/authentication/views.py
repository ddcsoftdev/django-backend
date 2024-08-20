from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from eshop.utils import handle_request
from .services import UserLoginService, UserLogoutService, UserSignupService


class UserLoginApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        """Handles login and generates token for authorised user."""
        login_service: UserLoginService = UserLoginService(request=request)
        return handle_request(login_service.login)


class UserLogoutApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        """Handles user logout and token invalidation."""
        logout_service: UserLogoutService = UserLogoutService(request=request)
        return handle_request(logout_service.logout)


class UserSignupApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        """Handles user registration."""
        signup_service: UserSignupService = UserSignupService(request=request)
        return handle_request(signup_service.signup)
