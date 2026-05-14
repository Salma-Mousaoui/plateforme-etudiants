"""
Models for the chat app.

Role : Real-time messaging (private and groups) via WebSocket.
"""

from django.db import models
from django.conf import settings


class ChatGroup(models.Model):
    """Discussion group by city or topic."""

    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100, blank=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chat_groups',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Chat Group'
        verbose_name_plural = 'Chat Groups'


class Message(models.Model):
    """Message sent in a private chat or a group."""

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent',
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='received',
        null=True,
        blank=True,
    )
    is_read = models.BooleanField(default=False)
    group = models.ForeignKey(
        ChatGroup,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True,
    )
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(
        upload_to='chat_attachments/',
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.group:
            return f"{self.sender.username} -> {self.group.name}: {self.content[:50]}"
        return f"{self.sender.username} -> {self.receiver.username}: {self.content[:50]}"

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['sent_at']
