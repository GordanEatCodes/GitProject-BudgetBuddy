from django.contrib import admin

# Register your models here.

# listing/admin.py
from django.contrib import admin
from .models import Room, Unit

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'rent', 'location', 'available', 'created_at')
    list_filter = ('available', 'has_internet', 'has_private_bathroom', 'near_station')
    search_fields = ('title', 'location', 'owner__username')

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'rent', 'location', 'bedrooms', 'bathrooms', 'available', 'created_at')
    list_filter = ('available', 'furnished', 'has_internet', 'near_station', 'pet_friendly')
    search_fields = ('title', 'location', 'owner__username')