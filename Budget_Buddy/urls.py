from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # User system / homepage / login / register / dashboard
    path('', include('users.urls')),

    # Rental / listing module
    path('listing/', include('listing.urls')),

    # Extra rental URL, in case your teammate uses /rentals/
    path('rentals/', include('listing.urls')),

    # Roommate module
    path('roommates/', include('roommate.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)