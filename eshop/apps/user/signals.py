from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update the UserProfile when a User is created or updated."""
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, "userprofile"):
            instance.userprofile.save()


@receiver(post_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    """Delete the UserProfile when the User is deleted."""
    if hasattr(instance, "userprofile"):
        instance.userprofile.delete()
