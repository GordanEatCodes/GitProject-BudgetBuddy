from django.contrib import admin
from .models import RoommatePost, RoommateApplication, RoommateMessage

admin.site.register(RoommatePost)
admin.site.register(RoommateApplication)
admin.site.register(RoommateMessage)