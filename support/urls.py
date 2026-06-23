from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('contact-us/', views.contact_us, name='contact_us'),
    path('contact_dash/', views.contact_dash, name='contact_dash'),
    path('chat/<int:session_id>/send/', views.send_message, name='send_message'),
    path('chat/<int:session_id>/messages/', views.poll_messages, name='poll_messages'),
    path('agent/inbox/', views.agent_inbox, name='agent_inbox'),
    path('agent/chat/<int:session_id>/', views.agent_chat, name='agent_chat'),
    path('agent/chat/<int:session_id>/claim/', views.agent_claim, name='agent_claim'),
    path('agent/chat/<int:session_id>/close/', views.agent_close_chat, name='agent_close_chat'),
]