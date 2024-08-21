from django.urls import path, re_path
from .views import *

# urls
login_url = r"^login/?$"
logout_url = r"^logout/?$"
signup_url = r"^signup/?$"

urlpatterns = [
    re_path(login_url, UserLoginApi().as_view(), name="login"),
    re_path(logout_url, UserLogoutApi().as_view(), name="logout"),
    re_path(signup_url, UserSignupApi().as_view(), name="signup"),
]
