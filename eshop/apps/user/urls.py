from django.urls import path, re_path
from django.conf import settings
from .views import *

urlpatterns = [
    re_path(
        r"^" + settings.API_URL + r"users/?$",
        UserProfileListAllApi().as_view(),
        name="user-list",
    ),
    re_path(
        r"^" + settings.API_URL + r"user-profile/?$",
        UserProfileDetailApi().as_view(),
        name="user-profile",
    ),
]
