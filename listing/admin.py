from django.contrib import admin
from .models import Room, Unit, RoomRequest, UnitRequest, RoomImage

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1  # 一次顯示幾列空白可以新增
    
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'state', 'city', 'unit_type', 'room_type', 'rent', 'available', 'created_at')
    list_filter = ('state', 'unit_type', 'room_type', 'available')
    search_fields = ('title', 'city', 'location_detail', 'owner__username')
    inlines = [RoomImageInline]



@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'state', 'unit_type', 'bedrooms', 'bathrooms', 'rent', 'available')
    list_filter = ('state', 'unit_type', 'bedrooms', 'bathrooms', 'available')
    search_fields = ('title', 'location_detail', 'owner__username')


@admin.register(RoomRequest)
class RoomRequestAdmin(admin.ModelAdmin):
    list_display = ('room', 'tenant', 'status', 'created_at', 'decision_at')
    list_filter = ('status', 'created_at')
    search_fields = ('room__title', 'tenant__username', 'tenant__email')


@admin.register(UnitRequest)
class UnitRequestAdmin(admin.ModelAdmin):
    list_display = ('unit', 'tenant', 'status', 'created_at', 'decision_at')
    list_filter = ('status', 'created_at')
    search_fields = ('unit__title', 'tenant__username', 'tenant__email')



