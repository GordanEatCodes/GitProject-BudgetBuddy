from django.urls import path
from . import views

urlpatterns = [
    # 選擇 Room / Unit 頁
    path('choose/', views.choose_view, name='choose'),

    # 列表頁
    path('rooms/', views.room_list, name='room_list'),
    path('units/', views.unit_list, name='unit_list'),

    # 房東後台 + 新增房間
    path('owner/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/rooms/new/', views.room_create, name='room_create'),
]
