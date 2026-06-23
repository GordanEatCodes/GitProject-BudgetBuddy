from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/',views.home, name='home'),

    path('about/', views.about, name='about'),

    path('register/', views.register_view, name='register'),
    path('register/otp/', views.register_otp_view, name='register_otp'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('forgot_password/verify/', views.reset_password_otp_view, name='reset_password_otp'),
    path('forgot_password/new-password/', views.reset_password_new_view, name='reset_password_new'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('setup_role/', views.setup_role_view, name='setup_role'),
    path('setup_profile/', views.setup_profile_view, name='setup_profile'),
    path('setup_tenant_preferences/', views.setup_tenant_preferences_view, name='setup_tenant_preferences'),
]