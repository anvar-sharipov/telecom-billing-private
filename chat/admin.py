from django.contrib import admin

from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'name', 'created_at')
    list_filter = ('type',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'text', 'is_deleted', 'created_at')
    list_filter = ('sender', 'is_deleted')
    search_fields = ('text',)
