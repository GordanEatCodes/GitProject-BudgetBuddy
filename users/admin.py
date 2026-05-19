from django.contrib import admin
from .models import User
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('Username', 'state', 'role', 'user')
    list_filter = ('role', 'state')
    search_fields = ('Username', 'state')




