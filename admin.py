# chatbot/admin.py
from django.contrib import admin
from .models import SessionContext, ChatAnalytics

@admin.register(SessionContext)
class SessionContextAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'last_intent', 'last_message', 'updated_at')
    search_fields = ('session_id', 'last_intent')

@admin.register(ChatAnalytics)
class ChatAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user_message', 'bot_response', 'response_time_ms', 'bias_detected', 'timestamp')
    list_filter = ('bias_detected', 'timestamp')
    search_fields = ('session_id', 'user_message')