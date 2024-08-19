from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .services import UserLoginService, UserLogoutService, UserSignupService


class UserLoginApi(APIView):
    """Handles login and generates token for authorised user"""

    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        login_service: UserLoginService = UserLoginService()
        try:
            return login_service.handle_login(request=request)
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)
            


class UserLogoutApi(APIView):
    """Handles user logout and token invalidation"""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        logout_service: UserLogoutService = UserLogoutService()
        try:
            return logout_service.handle_logout(request=request)
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class UserSignupApi(APIView):
    """Handles user registration"""

    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        try:
            return UserSignupService.handle_signup(request=request)
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)
