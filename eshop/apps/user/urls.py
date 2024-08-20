from django.urls import path, re_path
from django.conf import settings
from .views import *

# urls
users_url = r"^" + settings.API_URL + r"users/?$"
users_url_pk = r"^" + settings.API_URL + r"users/(?P<pk>\d+)/?$"
user_url = r"^" + settings.API_URL + r"user/?$"
user_url_pk = r"^" + settings.API_URL + r"user/(?P<pk>\d+)/?$"

urlpatterns = [
    re_path(users_url, UserProfileListAllApi().as_view(), name="users"),
    re_path(users_url_pk, UserProfileListAllApi().as_view(), name="users"),
    re_path(user_url, UserProfileRetrieveUpdateDestroyApi().as_view(), name="user"),
    re_path(user_url_pk, UserProfileRetrieveUpdateDestroyApi().as_view(), name="user"),
]
