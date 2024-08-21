from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from eshop.utils import build_response
from .serializers import UserProfileSerializer
from .models import UserProfile, User


class UserProfileDetailService:

    def __init__(self, request, pk=None):
        self.request = request
        self.user = request.user
        self.pk = pk

    def _get_target_user(self):
        """Retrieve the target user based on the provided pk or current user."""
        if self.pk:
            return User.objects.get(pk=self.pk)
        return self.user

    def _verify_user_access(self, target_user) -> bool:
        """Verify if the current user has access to the target user's profile."""
        if self.user.is_staff or self.user.is_superuser:
            return True
        return target_user == self.user

    def _logout_user(self, user):
        """Logout the user by deleting their token."""
        token = self.request.headers.get("Authorization", "").replace("Token ", "")
        if token:
            try:
                Token.objects.get(key=token).delete()
            except Token.DoesNotExist:
                pass

    def _check_user_hierarchy(self, user, restrict_superuser=False):
        """Check user auth hierarchy, lower cannot modify/delete higher."""
        if restrict_superuser and user.is_superuser:
            return build_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message="Admin user restricted",
            )
        if user.is_staff and not self.user.is_superuser:
            return build_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message="No access",
            )
        return None

    def get(self) -> Response:
        """Get the target user's profile. Admin/staff can get others profiles."""
        user = self._get_target_user()
        if not self._verify_user_access(user):
            return build_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message="Access to other users denied",
            )
        profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(profile)
        return build_response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self) -> Response:
        """Update the target user's profile. Admin/staff can update others profiles."""
        user = self._get_target_user()
        if not self._verify_user_access(user):
            return build_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message="Access to other users denied",
            )

        error = self._check_user_hierarchy(user=user)
        if error:
            return error

        profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(profile, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return build_response(status=status.HTTP_200_OK, data=serializer.data)
        return build_response(status=status.HTTP_409_CONFLICT, data=serializer.errors)

    def delete(self) -> Response:
        """Delete the target user's profile. Admin/staff can delete others profiles."""
        user = self._get_target_user()
        if not self._verify_user_access(user):
            return build_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message="Access to other users denied",
            )

        error = self._check_user_hierarchy(user=user, restrict_superuser=True)
        if error:
            return error

        self._logout_user(user=user)
        user.delete()
        return build_response(status=status.HTTP_204_NO_CONTENT)
