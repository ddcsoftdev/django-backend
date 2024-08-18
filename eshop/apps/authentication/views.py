from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, logout
from .serializers import LoginSerializer, LogoutSerializer, SignupSerializer

#TODO: 1. Fix the messages for erros in response message
#TODO 2. Check logic if user is already created.. also research if checks go in view or serializers
#TODO 3. Cleanup and move on to products

class LoginAPIView(APIView):
    """Handles login and generates token for authorised user"""

    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        serializer = LoginSerializer(data=request.data)
        # check if data is valid
        if serializer.is_valid():
            username: str = serializer.validated_data["username"]
            password: str = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)

            # check if user exists
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    "status": status.HTTP_201_CREATED,
                    "message": "User logged",
                    "data": {"Token": token.key if token is not None else created.key},
                }
                return Response(response, status=status.HTTP_201_CREATED)

            # if user does not exist
            response = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "Credentials incorrect",
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        # if data not valid
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Data invalid",
            "data": serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """Handles user logout and token invalidation"""

    permission_classes = [IsAuthenticated]
#TODO: NEED TO CLEAN THIS AND FIX ALL CODE WITH ERROR INSTEAD OF MESSAGE
    def post(self, request):
        token_key: str = request.headers.get("Authorization")
        if token_key is not None:
            token_key = token_key.split(" ")[1]
            token = Token.objects.get(key=token_key)
            if token.user is not None and token.user.is_authenticated:
                logout(request)
            token.delete()
            response = {"status": status.HTTP_204_NO_CONTENT, "message": "User logged out"}
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        
        #token not found
        response = {"status": status.HTTP_400_BAD_REQUEST, "error": "Token not found"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

        
        


class SignupAPIView(APIView):
    """Handles user registration"""

    # TODO DD(08/20/24): Add UserProfile Model on registry
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {"status": status.HTTP_201_CREATED, "message": "User created"}
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Data invalid",
            "data": serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
