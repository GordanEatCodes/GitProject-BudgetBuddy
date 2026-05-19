from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
# Create your models here.

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

ROLE_CHOICES = [
    ['owner', 'Owner'],
    ['tenant', 'Tenant'],
]

class UserProfile(models.Model):
    user = models. OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    gender = models.CharField(max_length=20, blank=True)
    sleep_schedule = models.CharField(max_length=20, blank=True)
    cleanliness = models.IntegerField(default=3)
    noise_tolerance = models.IntegerField(default=3)
    race = models.CharField(max_length=30, blank=True)
    religion = models.CharField(max_length=30, blank=True)
    study_habits = models.CharField(max_length=20, blank=True)

    Username       = models.CharField(max_length=60, blank=True)
    phone_number   = models.CharField(max_length=20, blank=True)
    state          = models.CharField(max_length=30, blank=True)
    bio            = models.TextField(blank=True)
