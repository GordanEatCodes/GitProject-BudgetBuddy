from django.db import models
from django.conf import settings

class Room(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    title = models.CharField(max_length=200)
    rent = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=255)

    size = models.CharField(max_length=50, blank=True, null=True)
    has_internet = models.BooleanField(default=False)
    has_private_bathroom = models.BooleanField(default=False)
    near_station = models.BooleanField(default=False)

    image = models.ImageField(upload_to='room_images/', blank=True, null=True)

    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Unit(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='units'
    )

    title = models.CharField(max_length=200)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)

    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, blank=True, null=True)

    furnished = models.BooleanField(default=False)
    has_internet = models.BooleanField(default=False)
    near_station = models.BooleanField(default=False)
    pet_friendly = models.BooleanField(default=False)

    image = models.ImageField(upload_to='unit_images/', blank=True, null=True)

    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
