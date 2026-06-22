from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from users.views import dashboard
from django.conf import settings
from django.conf.urls.static import static
from listing.views import home 
from users.views import about 
from users.views import about_dash

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('about/', about, name='about'),
    path('about_dash/',about_dash, name='about_dash'),
    path('users/', include('users.urls')),
    path('roommates/', include('roommate.urls')),
    path('listing/', include('listing.urls')),
    path('support/', include('support.urls')),
]

# Serve media & static in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
