from django.contrib import admin
from .models import Room, Unit

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    # Only using 'title' ensures it won't crash, no matter what fields Room has
    list_display = ('title',) 

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'rent', 'state', 'unit_type', 'available', 'created_at']
    list_filter = ['state', 'unit_type', 'available', 'has_wifi', 'pet_allowed']
    search_fields = ['title', 'location_detail']