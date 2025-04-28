# chatbot/models.py
from django.db import models
import json

class SessionContext(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    last_intent = models.CharField(max_length=50, blank=True, null=True)
    last_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session_id

    def __str__(self):
        return f"SessionContext for {self.session_id}"

class ChatAnalytics(models.Model):
    session_id = models.CharField(max_length=255)
    user_message = models.TextField()
    bot_response = models.TextField()
    response_time_ms = models.IntegerField()
    bias_detected = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analytics for Session {self.session_id} at {self.timestamp}"