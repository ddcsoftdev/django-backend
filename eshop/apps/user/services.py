from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from eshop.utils import build_response
from .serializers import *


class UserProfileDetailService:

    def __init__(self, request, pk=None):
        self.user = request.user
        self.queryset = UserProfile.objects.all()
        self.filters: dict = self._get_filter_criteria(request=request)
        self.pk = pk


    def _get_filter_criteria(self, request) -> dict:
        """Extracts filter criteria from request query parameters."""
        filter_criteria = {
            "user__id": request.query_params.get("user_id"),
            "user__username": request.query_params.get("username"),
            "user__email": request.query_params.get("email"),
        }
        return {key: value for key, value in filter_criteria.items() if value}

    @staticmethod
    def _logout_user(request):
        """Logs out user"""
        token_key = request.headers.get("Authorization", "").split(" ")[-1]
        try:
            token = Token.objects.get(key=token_key)
            token.delete()
        except Token.DoesNotExist as err:
            raise err

    def _try_get_profile(self, queryset, filters) -> Response:
        """Tries to get a profile and returns a response."""
        profile = self._get_filtered_profile(queryset=queryset, filters=filters)
        if profile:
            serializer = UserProfileSerializer(profile)
            return build_response(status_code=status.HTTP_200_OK, data=serializer.data)
        return build_response(
            status_code=status.HTTP_404_NOT_FOUND, message="User not found"
        )

    def _try_delete_profile(self, queryset, filters) -> Response:
        """Tries to delete a profile and returns a response."""
        profile = self._get_filtered_profile(queryset=queryset, filters=filters)
        if profile:
            profile.user.delete()
            return build_response(
                status_code=status.HTTP_200_OK,
                message="User deleted.",
            )
        return build_response(
            status_code=status.HTTP_404_NOT_FOUND, message="User not found"
        )

    @staticmethod
    def _try_update_profile(serializer) -> Response:
        """Tries to update a profile and returns a response."""
        if serializer.is_valid():
            serializer.save()
            return build_response(status_code=status.HTTP_200_OK, data=serializer.data)
        return build_response(
            status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors
        )

    def handle_get(self) -> Response:
        """Gets details with option to filter user_id, username and email."""
        if self.pk:
            pk_user = User.objects.get(pk=self.pk)
            data = UserProfile.objects.get(user=pk_user)
            serializer = UserProfileSerializer(data)
            return build_response(status=200, data=serializer.data)

        if not self.filters:
            profile = UserProfile.objects.get(user=self.user)
        elif not (self.user.is_staff or self.user.is_superuser):
            return build_response(status=401, message="Cannot access other users")
        else:
            profile = self.queryset.filter(**self.filters).first()

        if profile:
            serializer = UserProfileSerializer(profile)
            return build_response(status=200,data=serializer.data)
        return build_response(status_code=404, message="User not found")

    def handle_delete(self, request) -> Response:
        """Deletes a user profile filtered by user_id, username, or email."""
        user = request.user
        queryset = UserProfile.objects.all()
        filters = self._get_filter_criteria(request=request)

        if not filters:
            queryset = queryset.filter(user=user)
            self._logout_user(request=request)
        elif not (user.is_staff or user.is_superuser):
            return build_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Only admin or staff can delete other users",
            )

        return self._try_delete_profile(queryset=queryset, filters=filters)

    def handle_put(self, request) -> Response:
        """Handles PUT requests to update a user profile."""
        if not self.filters:
            profile = self.queryset.filter(user=self.user).first()
        elif not (self.user.is_staff or self.is_superuser):
            return build_response(status=401, message="Cannot update")
        else:
            profile = self._get_filtered_profile()

        if profile:
            serializer = UserProfileSerializer(profile, data=request.data)
            return self._try_update_profile(profile=profile, serializer=serializer)
        return build_response(status=404, message="User not found.")
