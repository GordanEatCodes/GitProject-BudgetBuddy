from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='roommates'),
    path('', views.roommate_list, name='roommates'),
    path('add/', views.add_roommate, name='add_roommate'),
    path('delete/<int:id>/', views.delete_roommate, name='delete_roommate'),
    path('edit/<int:id>/', views.edit_roommate, name='edit_roommate'),
    path('match/<int:id>/', views.match_roommates, name='match_roommates'),
]