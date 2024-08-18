from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .services import *


class UserLoginApi(APIView):
    """Handles login and generates token for authorised user"""

    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        login_service: UserLoginService = UserLoginService()
        return login_service.handle_login(request=request)


class UserLogoutApi(APIView):
    """Handles user logout and token invalidation"""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        logout_service: UserLogoutService = UserLogoutService()
        return logout_service.handle_logout(request=request)


class UserSignupApi(APIView):
    """Handles user registration"""

    # TODO DD(08/20/24): Add UserProfile Model on registry
    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        signup_service: UserSignupService = UserSignupService()
        return signup_service.handle_signup(request=request)
