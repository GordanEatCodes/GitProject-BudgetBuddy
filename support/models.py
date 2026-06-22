import uuid
from django.contrib.auth.models import User
from django.db import models


class ChatSession(models.Model):
    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [(STATUS_OPEN, 'Open'), (STATUS_CLOSED, 'Closed')]

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='chat_sessions')
    guest_id = models.CharField(max_length=36, null=True, blank=True, db_index=True)
    guest_name = models.CharField(max_length=100, blank=True)
    guest_email = models.EmailField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_OPEN)
    assigned_agent = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_chat_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_message_at']

    def __str__(self):
        owner = self.user.username if self.user else (self.guest_name or f"guest-{(self.guest_id or '')[:8]}")
        return f"Chat #{self.pk} with {owner}"


class ChatMessage(models.Model):
    SENDER_VISITOR = 'visitor'
    SENDER_AGENT = 'agent'
    SENDER_SYSTEM = 'system'
    SENDER_CHOICES = [(SENDER_VISITOR, 'Visitor'), (SENDER_AGENT, 'Agent'), (SENDER_SYSTEM, 'System')]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender_type = models.CharField(max_length=10, choices=SENDER_CHOICES)
    sender = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
