from django.urls import path, re_path
from django.conf import settings
from .views import *

# urls
login_url = r"^" + settings.API_URL + r"login/?$"
logout_url = r"^" + settings.API_URL + r"logout/?$"
signup_url = r"^" + settings.API_URL + r"signup/?$"

urlpatterns = [
    re_path(login_url, UserLoginApi().as_view(), name="login"),
    re_path(logout_url, UserLogoutApi().as_view(), name="logout"),
    re_path(signup_url, UserSignupApi().as_view(), name="signup"),
]
