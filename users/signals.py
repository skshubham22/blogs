# users/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import UserActivity

@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    UserActivity.objects.create(
        user=user, 
        action='login', 
        ip_address=request.META.get('REMOTE_ADDR')
    )

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    if user:
        UserActivity.objects.create(
            user=user, 
            action='logout', 
            ip_address=request.META.get('REMOTE_ADDR')
        )