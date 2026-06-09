"""
URL configuration for Budget_Buddy project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 💡 完美導入子視圖中的 home
from listing.views import home 

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL -> listing.views.home (this will handle fake role)
    path('', home, name='home'),

    path('users/', include('users.urls')),
    path('listing/', include('listing.urls')),
    
    # 💡 加上這行，可以防止隊友的登入限制導致 404 崩潰
    path('accounts/', include('django.contrib.auth.urls')), 
]

# Serve media & static in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
