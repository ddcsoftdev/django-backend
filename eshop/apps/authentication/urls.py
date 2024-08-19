from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path(settings.API_URL + 'login/', UserLoginApi().as_view(), name="user-login"),
    path(settings.API_URL + 'logout/', UserLogoutApi().as_view(), name="user-logout"),
    path(settings.API_URL + 'signup/', UserSignupApi().as_view(), name="user-signup"),
]
