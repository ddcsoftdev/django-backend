from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from eshop.utils import build_response
from .serializers import *


class UserProfileDetailService:

    def __init__(self, request, pk=None):
        self.request = request
        self.user = request.user
        self.queryset = UserProfile.objects.all()
        self.pk = pk

    def _get_target_user(self):
        if self.pk:
            return User.objects.get(pk=self.pk)
        return self.user

    def _verify_user_access(self, user) -> bool:
        if self.user.is_staff or self.user.is_superuser:
            return True
        elif user != self.user:
            return False

    def _logout_user(self, user):
        token: str = self.request.headers.get("Authorization", "")
        if token and token.startswith("Token "):
            token = token.split(" ")[-1]
            saved_token = Token.objects.get(key=token)
            if saved_token:
                saved_token.delete()

    def _check_user_hierarchy(self, user, r_admin=False):
        """Checks hirearchy bounds, r_admin restricts superuser."""
        if r_admin and user.is_superuser:
            return build_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message="Admin user restricted",
            )
        elif user.is_staff and not self.user.is_superuser:
            return build_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message="User hierarchy broken",
            )
        return None

    def get(self) -> Response:
        """Get user, access to other users restricted to admin/staff."""
        user = self._get_target_user()
        if self._verify_user_access(user) == False:
            return build_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message="Access to other users denied",
            )
        data = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(data)
        return build_response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self) -> Response:
        """Update user, access to other users restricted to admin/staff."""
        user = self._get_target_user()
        if self._verify_user_access(user) == False:
            return build_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message="Access to other users denied",
            )

        error = self._check_user_hierarchy(user=user, r_admin=False)
        if error is not None:
            return error

        profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(profile, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return build_response(status=status.HTTP_200_OK, data=serializer.data)
        return build_response(status=status.HTTP_409_CONFLICT, data=serializer.errors)

    def delete(self) -> Response:
        """Delete user, access to other users restricted to admin/staff."""
        user = self._get_target_user()
        if self._verify_user_access(user) == False:
            return build_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message="Access to other users denied",
            )

        error = self._check_user_hierarchy(user=user, r_admin=True)
        if error is not None:
            return error

        self._logout_user(user=user)
        user.delete()
        return build_response(status=status.HTTP_204_NO_CONTENT)
