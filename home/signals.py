from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from django.conf import settings

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=User)
def send_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'WELCOME TO TODOAPP',
            'Hi, you have successfully registered with TODOAPP.',
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False,
)
