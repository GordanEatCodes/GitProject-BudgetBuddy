from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')
        
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', lambda request: render(request, 'dashboard.html'), name='dashboard'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('users/', include('users.urls')),
    path('roommates/', include('roommate.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)