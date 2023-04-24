from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Cookbook

User = get_user_model()


@receiver(post_save, sender=User)
def create_cookbook(instance, created, **kwargs):
    if created:
        Cookbook.objects.create(user=instance)
