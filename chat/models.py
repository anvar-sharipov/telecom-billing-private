import uuid

from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

# Вложения в чат: любой тип файла (Excel, PDF, фото...), макс 20 МБ
ATTACHMENT_MAX_SIZE = 20 * 1024 * 1024


def message_attachment_path(instance, filename):
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
    new_filename = f'{uuid.uuid4()}.{ext}' if ext else str(uuid.uuid4())
    return f'chat_attachments/{instance.conversation_id}/{new_filename}'


class Conversation(models.Model):
    TYPE_DIRECT = 'direct'
    TYPE_GROUP = 'group'
    TYPE_CHOICES = [
        (TYPE_DIRECT, 'Direct'),
        (TYPE_GROUP, 'Group'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255, blank=True)  # только для group
    participants = models.ManyToManyField(User, related_name='chat_conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name or f'Direct #{self.pk}'


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='chat_sent_messages')
    text = models.TextField(blank=True)
    attachment = models.FileField(
        upload_to=message_attachment_path, blank=True, null=True)
    attachment_name = models.CharField(max_length=255, blank=True)
    attachment_size = models.PositiveIntegerField(null=True, blank=True)
    attachment_content_type = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Message #{self.pk} in Conversation #{self.conversation_id}'


class MessageRead(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='reads')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='chat_read_messages')
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('message', 'user')


class UserActivity(models.Model):
    # последняя активность — обновляется опросом бейджа чата с любой страницы (раз в ~20 сек)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='chat_activity')
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}: {self.last_seen}'


class TypingStatus(models.Model):
    # "X печатает..." — живёт несколько секунд, обновляется пока юзер набирает
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='typing')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('conversation', 'user')
