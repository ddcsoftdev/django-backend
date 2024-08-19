from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path(settings.API_URL + 'users', UserProfileListAllApi().as_view(), name="user-list"),
    path(settings.API_URL + 'user-profile', UserProfileDetailApi().as_view(), name="user-profile"),
]
