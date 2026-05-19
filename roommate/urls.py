from django.urls import path
from . import views

urlpatterns = [
    path('', views.roommate_list, name='roommate_list'),
    path('add/', views.add_roommate, name='add_roommate'),
    path('delete/<int:id>/', views.delete_roommate, name='delete_roommate'),
    path('edit/<int:id>/', views.edit_roommate, name='edit_roommate'),
]