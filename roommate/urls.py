from django.urls import path
from . import views

urlpatterns = [
    path('', views.roommate_list, name='roommate_list'),
    path('dashboard/', views.roommate_dashboard, name='roommate_dashboard'),
    path('add/', views.add_roommate, name='add_roommate'),
    path('detail/<int:id>/', views.roommate_detail, name='roommate_detail'),
    path('delete/<int:id>/', views.delete_roommate, name='delete_roommate'),
    path('edit/<int:id>/', views.edit_roommate, name='edit_roommate'),
    path('match/<int:id>/', views.match_roommates, name='match_roommates'),

    path('apply/<int:id>/', views.apply_roommate, name='apply_roommate'),
    path('applications-received/', views.applications_received, name='applications_received'),
    path('my-applications/', views.my_roommate_applications, name='my_roommate_applications'),

    path('application/<int:application_id>/', views.application_detail, name='application_detail'),
    path('application/<int:application_id>/messages/',views.get_chat_messages,name='get_chat_messages'),
    path('application/<int:application_id>/send/',views.send_chat_message,name='send_chat_message'),

    path(
        'application/<int:application_id>/cancel-accepted/',
        views.cancel_accepted_application,
        name='cancel_accepted_application'
    ),

    path(
        'application/<int:application_id>/<str:status>/',
        views.update_application_status,
        name='update_application_status'
    ),

    path('close/<int:id>/', views.close_roommate_post, name='close_roommate_post'),
    path('reopen/<int:id>/', views.reopen_roommate_post, name='reopen_roommate_post'),

    path('saved/', views.saved_roommate_posts, name='saved_roommate_posts'),
    path('favourite/<int:id>/', views.toggle_favourite, name='toggle_favourite'),
]