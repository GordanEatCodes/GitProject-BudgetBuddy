from django.db import models
from django.contrib.auth.models import User


class RoommatePost(models.Model):
    CLEANLINESS_CHOICES = [
        ('any', 'Any'),
        ('very_clean', 'Very Clean'),
        ('normal', 'Normal'),
        ('messy', 'Messy'),
    ]

    SLEEP_CHOICES = [
        ('any', 'Any'),
        ('early_sleep', 'Early Sleep'),
        ('late_sleep', 'Late Sleep'),
        ('flexible', 'Flexible'),
    ]

    STUDY_CHOICES = [
        ('any', 'Any'),
        ('quiet', 'Quiet Environment'),
        ('normal', 'Normal'),
        ('social', 'Social Environment'),
    ]

    SMOKING_CHOICES = [
        ('any', 'Any'),
        ('no_smoking', 'No Smoking'),
        ('smoking_ok', 'Smoking OK'),
    ]

    PET_CHOICES = [
        ('any', 'Any'),
        ('no_pets', 'No Pets'),
        ('pets_ok', 'Pets OK'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    budget = models.FloatField()
    contact = models.CharField(max_length=100)

    cleanliness = models.CharField(max_length=20, choices=CLEANLINESS_CHOICES, default='any')
    sleep_schedule = models.CharField(max_length=20, choices=SLEEP_CHOICES, default='any')
    study_preference = models.CharField(max_length=20, choices=STUDY_CHOICES, default='any')
    smoking = models.CharField(max_length=20, choices=SMOKING_CHOICES, default='any')
    pets = models.CharField(max_length=20, choices=PET_CHOICES, default='any')

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title