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

    POST_STATUS_CHOICES = [
        ('open', 'Open'),
        ('full', 'Full'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    budget = models.FloatField()
    contact = models.CharField(max_length=100)

    unit_name = models.CharField(max_length=100, blank=True)
    total_rent = models.FloatField(null=True, blank=True)
    total_people = models.PositiveIntegerField(default=1)
    needed_roommates = models.PositiveIntegerField(default=1)

    post_status = models.CharField(
        max_length=20,
        choices=POST_STATUS_CHOICES,
        default='open'
    )

    cleanliness = models.CharField(max_length=20, choices=CLEANLINESS_CHOICES, default='any')
    sleep_schedule = models.CharField(max_length=20, choices=SLEEP_CHOICES, default='any')
    study_preference = models.CharField(max_length=20, choices=STUDY_CHOICES, default='any')
    smoking = models.CharField(max_length=20, choices=SMOKING_CHOICES, default='any')

    # Basic pet preference
    pets = models.CharField(
        max_length=20,
        choices=PET_CHOICES,
        default='any'
    )

    # NEW: More detailed pet preference
    preferred_pet = models.CharField(
        max_length=150,
        blank=True,
        help_text="Example: Cats, Small Dogs, Rabbit, Fish"
    )

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def accepted_roommates_count(self):
        return self.applications.filter(status='accepted').count()

    def remaining_roommates_needed(self):
        remaining = self.needed_roommates - self.accepted_roommates_count()
        return max(remaining, 0)

    def save(self, *args, **kwargs):
        if self.total_rent and self.total_people and self.total_people > 0:
            self.budget = round(self.total_rent / self.total_people, 2)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class RoommateApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    roommate_post = models.ForeignKey(
        RoommatePost,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='roommate_applications'
    )

    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('roommate_post', 'applicant')

    def __str__(self):
        return f"{self.applicant.username} applied for {self.roommate_post.title}"


class RoommateMessage(models.Model):
    application = models.ForeignKey(
        RoommateApplication,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username}"


class RoommateFavourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='roommate_favourites'
    )

    roommate_post = models.ForeignKey(
        RoommatePost,
        on_delete=models.CASCADE,
        related_name='favourites'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'roommate_post')

    def __str__(self):
        return f"{self.user.username} saved {self.roommate_post.title}"