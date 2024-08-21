from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """User Profile that extends the User model with additional information."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    credit_card = models.CharField(max_length=14, blank=True)
    address = models.CharField(max_length=200, blank=True)
    mobile = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username
