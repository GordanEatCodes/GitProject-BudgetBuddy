from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from users.views import dashboard
from django.conf import settings
from django.conf.urls.static import static
from listing.views import home 

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('users/', include('users.urls')),
    path('roommates/', include('roommate.urls')),
    path('listing/', include('listing.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

]

# Serve media & static in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
