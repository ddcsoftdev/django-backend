from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import UserProfile
from eshop.utils import handle_request
from .serializers import UserProfileSerializer
from .filters import UserProfileFilter
from .services import UserProfileDetailService


class UserProfileListAllApi(generics.ListAPIView):
    """Lists all registered users, accessible only by admin/staff."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserProfileFilter

    def get_queryset(self):
        """Override to filter by user ID if provided."""
        queryset = super().get_queryset()
        pk = self.kwargs.get("pk")
        if pk:
            queryset = queryset.filter(user_id=pk)
        return queryset


class UserProfileRetrieveUpdateDestroyApi(APIView):
    """Handles retrieving, updating, or deleting a user profile."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None) -> Response:
        """Retrieve user profile details; admin/staff can retrieve others."""
        user_service = UserProfileDetailService(request=request, pk=pk)
        return handle_request(user_service.get)

    def put(self, request, pk=None) -> Response:
        """Update user profile details; admin/staff can update others."""
        user_service = UserProfileDetailService(request=request, pk=pk)
        return handle_request(user_service.put)

    def delete(self, request, pk=None) -> Response:
        """Delete user profile; admin/staff can delete others."""
        user_service = UserProfileDetailService(request=request, pk=pk)
        return handle_request(user_service.delete)
