from django.db import models
from django.conf import settings


class Room(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    from django.db import models
from django.conf import settings


MALAYSIA_STATES = [
    ('Johor', 'Johor'),
    ('Kedah', 'Kedah'),
    ('Kelantan', 'Kelantan'),
    ('Melaka', 'Melaka'),
    ('Negeri Sembilan', 'Negeri Sembilan'),
    ('Pahang', 'Pahang'),
    ('Perak', 'Perak'),
    ('Perlis', 'Perlis'),
    ('Pulau Pinang', 'Pulau Pinang'),
    ('Sabah', 'Sabah'),
    ('Sarawak', 'Sarawak'),
    ('Selangor', 'Selangor'),
    ('Terengganu', 'Terengganu'),
    ('WP Kuala Lumpur', 'WP Kuala Lumpur'),
    ('WP Labuan', 'WP Labuan'),
    ('WP Putrajaya', 'WP Putrajaya'),
]

UNIT_TYPES = [
    ('Studio', 'Studio'),
    ('Duplex', 'Duplex'),
    ('Triplex', 'Triplex'),
    ('Condo', 'Condo'),
    ('Apartment', 'Apartment'),
    ('Terrace', 'Terrace'),
    ('Semi-D', 'Semi-D'),
    ('Bungalow', 'Bungalow'),
    ('Others', 'Others'),
]

FLOOR_LEVELS = [
    ('Ground', 'Ground'),
    ('1-10', 'Level 1–10'),
    ('11-20', 'Level 11–20'),
    ('21-30', 'Level 21–30'),
    ('31+', 'Level 31+'),
]


class Room(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    title = models.CharField(max_length=200)
    rent = models.DecimalField(max_digits=8, decimal_places=2)

    # Location
    state = models.CharField(max_length=30, choices=MALAYSIA_STATES)
    location_detail = models.CharField(
        max_length=255,
        blank=True,
        help_text="City / area / address details"
    )

    # Unit type + floor (same choices as Unit)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPES)
    floor_level = models.CharField(max_length=10, choices=FLOOR_LEVELS)

    # Bathroom type for Room
    BATHROOM_TYPE_CHOICES = [
        ('shared', 'Shared bathroom'),
        ('private', 'Private bathroom'),
    ]
    bathroom_type = models.CharField(
        max_length=10,
        choices=BATHROOM_TYPE_CHOICES,
        default='shared'
    )

    # Strategies (near transport/facilities)
    near_mrt = models.BooleanField(default=False)
    near_lrt = models.BooleanField(default=False)
    near_ktm = models.BooleanField(default=False)
    near_bus_stop = models.BooleanField(default=False)
    near_brt = models.BooleanField(default=False)
    security_24h = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    gym_room = models.BooleanField(default=False)
    covered_carpark = models.BooleanField(default=False)
    near_mall = models.BooleanField(default=False)
    near_shop_lots = models.BooleanField(default=False)
    near_convenience_store = models.BooleanField(default=False)

    # Utilities (same as Unit)
    has_aircond = models.BooleanField(default=False)
    has_washing_machine = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    cooking_allowed = models.BooleanField(default=False)
    shared_bathroom = models.BooleanField(default=False)
    private_bathroom = models.BooleanField(default=False)
    has_tv = models.BooleanField(default=False)
    has_fridge = models.BooleanField(default=False)

    # Flexibility
    pet_allowed = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)

    # General
    size = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 10 m²")
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

    # Location
    state = models.CharField(max_length=30, choices=MALAYSIA_STATES)
    location_detail = models.CharField(
        max_length=255,
        blank=True,
        help_text="City / area / address details"
    )

    # Unit type + floor
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPES)
    floor_level = models.CharField(max_length=10, choices=FLOOR_LEVELS)

    BEDROOM_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3-5', '3–5'),
        ('5+', '5+'),
    ]
    BATHROOM_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3-5', '3–5'),
        ('5+', '5+'),
    ]
    bedrooms = models.CharField(max_length=4, choices=BEDROOM_CHOICES)
    bathrooms = models.CharField(max_length=4, choices=BATHROOM_CHOICES)

    # Strategies
    near_mrt = models.BooleanField(default=False)
    near_lrt = models.BooleanField(default=False)
    near_ktm = models.BooleanField(default=False)
    near_bus_stop = models.BooleanField(default=False)
    near_brt = models.BooleanField(default=False)
    security_24h = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    gym_room = models.BooleanField(default=False)
    covered_carpark = models.BooleanField(default=False)
    near_mall = models.BooleanField(default=False)
    near_shop_lots = models.BooleanField(default=False)
    near_convenience_store = models.BooleanField(default=False)

    # Utilities
    has_aircond = models.BooleanField(default=False)
    has_washing_machine = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    cooking_allowed = models.BooleanField(default=False)
    shared_bathroom = models.BooleanField(default=False)
    private_bathroom = models.BooleanField(default=False)
    has_tv = models.BooleanField(default=False)
    has_fridge = models.BooleanField(default=False)

    # Flexibility
    pet_allowed = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)

    # General
    size = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 80 m²")
    image = models.ImageField(upload_to='unit_images/', blank=True, null=True)

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

    # 0. Location (states in Malaysia)
    MALAYSIA_STATES = [
        ('Johor', 'Johor'),
        ('Kedah', 'Kedah'),
        ('Kelantan', 'Kelantan'),
        ('Melaka', 'Melaka'),
        ('Negeri Sembilan', 'Negeri Sembilan'),
        ('Pahang', 'Pahang'),
        ('Perak', 'Perak'),
        ('Perlis', 'Perlis'),
        ('Pulau Pinang', 'Pulau Pinang'),
        ('Sabah', 'Sabah'),
        ('Sarawak', 'Sarawak'),
        ('Selangor', 'Selangor'),
        ('Terengganu', 'Terengganu'),
        ('WP Kuala Lumpur', 'WP Kuala Lumpur'),
        ('WP Labuan', 'WP Labuan'),
        ('WP Putrajaya', 'WP Putrajaya'),
    ]
    state = models.CharField(max_length=30, choices=MALAYSIA_STATES)
    location_detail = models.CharField(
        max_length=255,
        blank=True,
        help_text="City / area / address details"
    )

    # 1. Unit Type
    UNIT_TYPES = [
        ('Studio', 'Studio'),
        ('Duplex', 'Duplex'),
        ('Triplex', 'Triplex'),
        ('Condo', 'Condo'),
        ('Apartment', 'Apartment'),
        ('Terrace', 'Terrace'),
        ('Semi-D', 'Semi-D'),
        ('Bungalow', 'Bungalow'),
        ('Others', 'Others'),
    ]
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPES)

    # 2. Floor level
    FLOOR_LEVELS = [
        ('Ground', 'Ground'),
        ('1-10', 'Level 1–10'),
        ('11-20', 'Level 11–20'),
        ('21-30', 'Level 21–30'),
        ('31+', 'Level 31+'),
    ]
    floor_level = models.CharField(max_length=10, choices=FLOOR_LEVELS)

    # 3. Bedrooms
    BEDROOM_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3-5', '3–5'),
        ('5+', '5+'),
    ]
    bedrooms = models.CharField(max_length=4, choices=BEDROOM_CHOICES)

    # 4. Bathrooms
    BATHROOM_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3-5', '3–5'),
        ('5+', '5+'),
    ]
    bathrooms = models.CharField(max_length=4, choices=BATHROOM_CHOICES)

    # 4. Strategies (near transport/facilities)
    near_mrt = models.BooleanField(default=False)
    near_lrt = models.BooleanField(default=False)
    near_ktm = models.BooleanField(default=False)
    near_bus_stop = models.BooleanField(default=False)
    near_brt = models.BooleanField(default=False)
    security_24h = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    gym_room = models.BooleanField(default=False)
    covered_carpark = models.BooleanField(default=False)
    near_mall = models.BooleanField(default=False)
    near_shop_lots = models.BooleanField(default=False)
    near_convenience_store = models.BooleanField(default=False)

    # 5. Utilities
    has_aircond = models.BooleanField(default=False)
    has_washing_machine = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    cooking_allowed = models.BooleanField(default=False)
    shared_bathroom = models.BooleanField(default=False)
    private_bathroom = models.BooleanField(default=False)
    has_tv = models.BooleanField(default=False)
    has_fridge = models.BooleanField(default=False)

    # 6. Flexibility
    pet_allowed = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)

    # General
    size = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 80 m²")
    image = models.ImageField(upload_to='unit_images/', blank=True, null=True)

    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
