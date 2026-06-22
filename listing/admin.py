from django.contrib import admin
from .models import Room, Unit

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    # 只保留绝对安全的字段，不碰 state、has_wifi
    list_display = ['title', 'owner', 'rent', 'available', 'created_at']
    search_fields = ['title', 'owner__username']

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    # Unit 已经做过 migration 了，所以可以用这些字段
    list_display = ['title', 'owner', 'rent', 'state', 'unit_type', 'available', 'created_at']
    list_filter = ['state', 'unit_type', 'available', 'has_wifi', 'pet_allowed']
    search_fields = ['title', 'location_detail']