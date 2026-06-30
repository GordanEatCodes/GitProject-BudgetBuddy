from django.urls import path
from . import views

urlpatterns = [

    path('choose/', views.choose_view, name='choose'),

    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),

    path('units/', views.unit_list, name='unit_list'),
    path('units/<int:pk>/', views.unit_detail, name='unit_detail'),

    path('owner/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/rooms/new/', views.room_create, name='room_create'),
    path('owner/units/new/', views.unit_create, name='unit_create'),

    path('owner/requests/<int:request_id>/<str:action>/',
         views.room_request_action,
         name='room_request_action'),

    path('owner/unit-requests/<int:request_id>/<str:action>/',
         views.unit_request_action,
         name='unit_request_action'),

    path('my-requests/rooms/', views.my_room_requests, name='my_room_requests'),
    
        # Room 編輯 / 上下架
    path('owner/rooms/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('owner/rooms/<int:pk>/toggle/', views.room_toggle_available, name='room_toggle_available'),

]

