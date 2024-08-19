from django.urls import path, re_path
from django.conf import settings
from .views import *

urlpatterns = [
    re_path(r'^' + settings.API_URL + r'login/?$', UserLoginApi().as_view(), name="user-login"),
    re_path(r'^' + settings.API_URL + r'logout/?$', UserLogoutApi().as_view(), name="user-logout"),
    re_path(r'^' + settings.API_URL + r'signup/?$', UserSignupApi().as_view(), name="user-signup"),
]
