from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path(settings.API_URL + 'login/', LoginAPIView().as_view(), name="user-login"),
    path(settings.API_URL + 'logout/', LogoutAPIView().as_view(), name="user-logout"),
    path(settings.API_URL + 'signup/', SignupAPIView().as_view(), name="user-signup"),
]
