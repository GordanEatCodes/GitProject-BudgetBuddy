from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    ROLE_CHOICES = [
    ('owner', 'house owner'),
    ('coordinator', 'main coordinator'),
    ('tenant', 'primary tenant'),
]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    gender = models.CharField(max_length=10, blank=True, null=True)
    sleep_schedule = models.CharField(max_length=20, blank=True)
    cleanliness = models.CharField(max_length=20, blank=True)
    noise_tolerance = models.CharField(max_length=20, blank=True)
    guest_frequency = models.CharField(max_length=20, blank=True)
    smoking_preference = models.CharField(max_length=20, blank=True)
    religion = models.CharField(max_length=20, blank=True)
    study_habits = models.CharField(max_length=20, blank=True)


