from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import UserProfile
from rest_framework import status
from .serializers import UserProfileSerializer
from .filters import UserProfileFilter
from .services import UserProfileDetailService


class UserProfileListAllApi(generics.ListAPIView):
    """Lists all registered users, accessible only if admin/staff."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserProfileFilter


class UserProfileDetailApi(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserProfileDetailService()

    def get(self, request) -> Response:
        """Allows users to retrieve their profile details, or others if admin/staff."""
        return self._handle_request(self.user_service.handle_get, request)

    def put(self, request) -> Response:
        """Allows users to update their profile details, or others if admin/staff."""
        return self._handle_request(self.user_service.handle_put, request)

    def delete(self, request) -> Response:
        """Allows users to delete their profile, or others if admin/staff."""
        return self._handle_request(self.user_service.handle_delete, request)

    def _handle_request(self, service_method, request) -> Response:
        """Handles exceptions for the service methods."""
        try:
            return service_method(request=request)
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)
