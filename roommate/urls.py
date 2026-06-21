from django.urls import path
from . import views

urlpatterns = [
    path('', views.roommate_list, name='roommate_list'),
    path('add/', views.add_roommate, name='add_roommate'),
    path('detail/<int:id>/', views.roommate_detail, name='roommate_detail'),
    path('delete/<int:id>/', views.delete_roommate, name='delete_roommate'),
    path('edit/<int:id>/', views.edit_roommate, name='edit_roommate'),
    path('match/<int:id>/', views.match_roommates, name='match_roommates'),

    path('apply/<int:id>/', views.apply_roommate, name='apply_roommate'),
    path('applications-received/', views.applications_received, name='applications_received'),
    path('my-applications/', views.my_roommate_applications, name='my_roommate_applications'),
    path('application/<int:application_id>/', views.application_detail, name='application_detail'),
    path('application/<int:application_id>/<str:status>/', views.update_application_status, name='update_application_status'),
]