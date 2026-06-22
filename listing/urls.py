from django.urls import path
from . import views

urlpatterns = [
    path('choose/', views.choose_view, name='choose'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('units/', views.unit_list, name='unit_list'),
    

    path('owner/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/rooms/new/', views.room_create, name='room_create'),
    path('owner/units/new/', views.unit_create, name='unit_create'),
]
