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
    """Lists all registered users, auth only for staff or superuser"""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserProfileFilter


class UserProfileDetailApi(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """Only allowed to get self user, unless admin or staff"""  
        user_service: UserProfileDetailService = UserProfileDetailService()
        try:
            return user_service.handle_get(request=request)
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)     

    def put(self, request) -> Response:
        """Only allowed to update self user, unless admin or staff"""
        user_service: UserProfileDetailService = UserProfileDetailService()
        try:
            return user_service.handle_put(request=request)
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request) -> Response:
        """Only allowed to delete self user, unless admin or staff"""
        user_service: UserProfileDetailService = UserProfileDetailService()
        try:
            return user_service.handle_delete(request=request)
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)  


class UserCreation(APIView):
    """This endpoint is only auth for admin or staff"""

    permission_classes = [IsAdminUser]

    def post(self, request) -> Response:
        pass
 
