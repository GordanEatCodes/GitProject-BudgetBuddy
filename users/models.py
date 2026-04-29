from django.db import models
from django.contrib.auth.models import User
# Create your models here.

ROLE_CHOICES = [
    ['owner', 'Owner'],
    ['tenant', 'Tenant'],
    ['coordinator', 'Coordinator'],
]

RENTAL_METHOD_CHOICES = [
    ('direct', 'Direct Room Rental'),
    ('coordinator', 'Whole Unit Rental through Coordinator'),
]

TENANT_TYPE_CHOICES = [
    ('direct', 'Direct Tenant'),
    ('matching', 'Matching Tenant System'),
]

class UserProfile(models.Model):
    user = models. OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    rental_method = models.CharField(
        max_length=20, 
        choices=RENTAL_METHOD_CHOICES,
        blank=True,
    )

    tenant_type = models.CharField(
        max_length=20,
        choices=TENANT_TYPE_CHOICES,
        blank=True,
    )

    gender = models.CharField(max_length=20, blank=True)
    sleep_schedule = models.CharField(max_length=20, blank=True)
    cleanliness = models.IntegerField(default=3)
    noise_tolerance = models.IntegerField(default=3)
    religion = models.CharField(max_length=30, blank=True)
    study_habits = models.CharField(max_length=20, blank=True)