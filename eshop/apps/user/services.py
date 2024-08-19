from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *


def build_response(status_code, message=None, data=None) -> Response:
    """Builds and returns a standard response format"""
    response_data = {"status": status_code}

    if message:
        response_data["message"] = message
    if data:
        response_data["data"] = data

    return Response(response_data, status=status_code)


class UserProfileDetailService:

    @staticmethod
    def _get_filter_criteria(request) -> dict:
        """Extracts filter criteria from request query parameters."""
        filter_criteria = {}
        user_id = request.query_params.get("user_id")
        username = request.query_params.get("username")
        email = request.query_params.get("email")

        if user_id:
            filter_criteria["user__id"] = user_id
        if username:
            filter_criteria["user__username"] = username
        if email:
            filter_criteria["user__email"] = email

        return filter_criteria

    @staticmethod
    def _get_filtered_profile(queryset, filters: dict) -> UserProfile:
        """Fetches a single user profile based on the provided filters."""
        if filters:
            return queryset.get(**filters)
        return queryset.first()

    @staticmethod
    def _logout_user(request):
        """Logs out user"""
        token_key = request.headers.get("Authorization", "").split(" ")[-1]
        token = Token.objects.get(key=token_key)
        if token:
            token.delete()

    def handle_get(self, request) -> Response:
        """Gets details with option to filter user_id, username and email."""
        user = request.user
        queryset = UserProfile.objects.all()

        filters: dict = self._get_filter_criteria(request=request)
        if not filters:
            queryset = queryset.filter(user=user)
        elif not (user.is_staff or user.is_superuser):
            return build_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Cannot access other users",
            )

        try:
            profile = self._get_filtered_profile(queryset=queryset, filters=filters)
            serializer = UserProfileSerializer(profile)
            return build_response(status_code=status.HTTP_200_OK, data=serializer.data)
        except Exception as err:
            return build_response(status_code=status.HTTP_404_NOT_FOUND, data=str(err))

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

        try:
            profile = self._get_filtered_profile(queryset=queryset, filters=filters)
            profile.user.delete()
            return build_response(
                status_code=status.HTTP_200_OK,
                message="User deleted.",
            )
        except Exception as err:
            return build_response(status_code=status.HTTP_404_NOT_FOUND, data=str(err))

    def handle_put(self, request) -> Response:
        """Handles PUT requests to update a user profile."""
        filters = self._get_filter_criteria(request=request)
        queryset = UserProfile.objects.all()
        user = request.user
        
        if not filters:
            profile = queryset.filter(user=user).first()
        elif not (user.is_staff or user.is_superuser):
            return build_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Cannot update other users' profiles",
            )
        else:
            profile = self._get_filtered_profile(queryset=queryset, filters=filters)

        if not profile:
            return build_response(
                status_code=status.HTTP_404_NOT_FOUND, message="Profile not found."
            )

        serializer = UserProfileSerializer(
            profile, data=request.data
        )

        
        if serializer.is_valid():
            serializer.save()
            return build_response(status_code=status.HTTP_200_OK, data=serializer.data)
        else:
            return build_response(
                status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )
