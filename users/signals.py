from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from queries.common.access import create_api_key
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            api_key=create_api_key()
        )


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
