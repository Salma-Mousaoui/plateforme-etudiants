"""
Models for the chat app.

Role : Messagerie en temps réel (privée et groupes) via WebSocket.
"""

from django.db import models
from django.conf import settings


class ChatGroup(models.Model):
    """Groupe de discussion par ville ou thématique."""

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
        verbose_name = 'Groupe de discussion'
        verbose_name_plural = 'Groupes de discussion'


class Message(models.Model):
    """Message envoyé dans un chat privé ou un groupe."""

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
        null=True,
        blank=True,
    )
    group = models.ForeignKey(
        ChatGroup,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True,
    )
    content    = models.TextField()
    is_read    = models.BooleanField(default=False)
    attachment = models.FileField(upload_to="chat_attachments/", blank=True, null=True)
    sent_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.group:
            return f"{self.sender.username} -> {self.group.name}: {self.content[:50]}"
        return f"{self.sender.username} -> {self.receiver.username}: {self.content[:50]}"

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['sent_at']
