from django.urls import path, re_path
from django.conf import settings
from .views import *

base_url: str = settings.API_URL

urlpatterns = [
    re_path(
        r"^" + base_url + r"users/?$",
        UserProfileListAllApi().as_view(),
        name="user-list",
    ),
    re_path(
        r"^" + base_url + r"user-profile/?$",
        UserProfileDetailApi().as_view(),
        name="user-profile",
    ),
    re_path(
        r"^" + base_url + r"user-profile/(?P<pk>\d+)/$",
        UserProfileDetailApi().as_view(),
        name="user-profile",
    ),
]
