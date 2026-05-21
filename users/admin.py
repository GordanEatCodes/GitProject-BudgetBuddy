from django.contrib import admin
from .models import User
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'state', 'role', 'user')
    list_filter = ('role', 'state')
    search_fields = ('username', 'state')




