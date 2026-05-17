"""
Admin configuration for the chat app.
"""

from django.contrib import admin

from .models import ChatGroup, Message


@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display  = ("name", "city", "member_count", "created_at")
    list_filter   = ("city",)
    search_fields = ("name", "city")
    filter_horizontal = ("members",)

    @admin.display(description="Members")
    def member_count(self, obj):
        return obj.members.count()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display  = ("sender", "receiver", "group", "content_preview", "sent_at", "is_read")
    list_filter   = ("is_read",)
    search_fields = ("sender__username", "content")
    raw_id_fields = ("sender", "receiver", "group")

    @admin.display(description="Content")
    def content_preview(self, obj):
        return obj.content[:60]
