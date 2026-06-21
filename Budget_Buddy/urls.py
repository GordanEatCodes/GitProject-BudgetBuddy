from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Temporary login/logout for testing
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Temporary dashboard for testing
    path('dashboard/', lambda request: redirect('/roommates/'), name='dashboard'),

    path('', include('users.urls')),
    path('roommates/', include('roommate.urls')),
]