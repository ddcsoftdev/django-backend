from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """User Profile that extends each User Model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit_card = models.CharField(max_length=14, blank=True)
    address = models.CharField(max_length=200,  blank=True)
    mobile = models.CharField(max_length=15,  blank=True)

    def __str__(self):
        return self.user.username
    
    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username
    
    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name