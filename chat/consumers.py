import json
from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import ChatGroup, Message

User = get_user_model()

# Redis is a pub/sub bus, not a file transfer protocol.
# Keeping payloads under 512 KB ensures we never hit the channel layer's
# default capacity limit and prevents accidental binary blobs from reaching Redis.
MAX_WS_PAYLOAD = 512 * 1024  # 512 KB


class PrivateChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        self.other_user_id = int(self.scope["url_route"]["kwargs"]["other_user_id"])
        u1 = min(user.id, self.other_user_id)
        u2 = max(user.id, self.other_user_id)
        self.room_name = f"chat_{u1}_{u2}"

        try:
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.accept()
            history = await self.get_history(user.id, self.other_user_id)
            for msg in history:
                await self.send(text_data=json.dumps(msg))
            await self.mark_messages_read(user, self.other_user_id)
        except Exception:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "room_name"):
            try:
                await self.channel_layer.group_discard(self.room_name, self.channel_name)
            except Exception:
                pass

    async def receive(self, text_data):
        # Hard-reject oversized payloads before they touch Redis.
        if len(text_data.encode("utf-8")) > MAX_WS_PAYLOAD:
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "Message too large. Please upload images using the attachment button.",
            }))
            return

        try:
            data = json.loads(text_data)
        except (json.JSONDecodeError, ValueError):
            return

        msg_type = data.get("type", "text")
        user = self.scope["user"]

        if msg_type == "image_url":
            url = data.get("url", "").strip()
            if not url:
                return
            # The Message record was already created by ChatImageUploadView
            # (HTTP POST). The consumer's only job here is real-time delivery.
            await self.channel_layer.group_send(self.room_name, {
                "type": "chat_message",
                "msg_type": "image_url",
                "url": url,
                "sender_id": user.id,
                "sender_name": user.get_full_name() or user.username,
                "sent_at": datetime.now().strftime("%H:%M"),
            })
        else:
            content = data.get("message", "").strip()
            if not content:
                return
            msg = await self.save_message(user, self.other_user_id, content)
            if msg is None:
                return
            await self.channel_layer.group_send(self.room_name, {
                "type": "chat_message",
                "msg_type": "text",
                "message": content,
                "sender_id": user.id,
                "sender_name": user.get_full_name() or user.username,
                "sent_at": datetime.now().strftime("%H:%M"),
                "is_read": False,
            })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_history(self, user_id, other_user_id):
        messages = list(
            Message.objects.filter(
                Q(sender_id=user_id, receiver_id=other_user_id) |
                Q(sender_id=other_user_id, receiver_id=user_id)
            ).select_related('sender').order_by('sent_at')
        )[-50:]
        return [
            {
                "type": "history_item",
                "message": msg.content,
                "sender_id": msg.sender_id,
                "sender_name": msg.sender.get_full_name() or msg.sender.username,
                "sent_at": msg.sent_at.strftime("%H:%M"),
                "is_read": msg.is_read,
            }
            for msg in messages
        ]

    @database_sync_to_async
    def save_message(self, sender, receiver_id, content):
        try:
            receiver = User.objects.get(id=receiver_id)
            return Message.objects.create(sender=sender, receiver=receiver, content=content)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def mark_messages_read(self, user, other_user_id):
        Message.objects.filter(
            receiver=user,
            sender_id=other_user_id,
            is_read=False,
        ).update(is_read=True)


class GroupChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        self.group_id = int(self.scope["url_route"]["kwargs"]["group_id"])
        self.room_name = f"groupe_{self.group_id}"

        try:
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.accept()
            await self.ensure_member(user, self.group_id)
            history = await self.get_history(self.group_id)
            for msg in history:
                await self.send(text_data=json.dumps(msg))
        except Exception:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "room_name"):
            try:
                await self.channel_layer.group_discard(self.room_name, self.channel_name)
            except Exception:
                pass

    async def receive(self, text_data):
        if len(text_data.encode("utf-8")) > MAX_WS_PAYLOAD:
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "Message too large. Please upload images using the attachment button.",
            }))
            return

        try:
            data = json.loads(text_data)
        except (json.JSONDecodeError, ValueError):
            return

        content = data.get("message", "").strip()
        if not content:
            return

        user = self.scope["user"]

        msg = await self.save_group_message(user, self.group_id, content)
        if msg is None:
            return

        await self.channel_layer.group_send(self.room_name, {
            "type": "chat_message",
            "msg_type": "text",
            "message": content,
            "sender_id": user.id,
            "sender_name": user.get_full_name() or user.username,
            "sent_at": datetime.now().strftime("%H:%M"),
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def ensure_member(self, user, group_id):
        try:
            group = ChatGroup.objects.get(id=group_id)
            if not group.members.filter(pk=user.pk).exists():
                group.members.add(user)
        except ChatGroup.DoesNotExist:
            pass

    @database_sync_to_async
    def get_history(self, group_id):
        messages = list(
            Message.objects.filter(group_id=group_id)
            .select_related('sender')
            .order_by('sent_at')
        )[-50:]
        return [
            {
                "type": "history_item",
                "message": msg.content,
                "sender_id": msg.sender_id,
                "sender_name": msg.sender.get_full_name() or msg.sender.username,
                "sent_at": msg.sent_at.strftime("%H:%M"),
            }
            for msg in messages
        ]

    @database_sync_to_async
    def save_group_message(self, sender, group_id, content):
        try:
            group = ChatGroup.objects.get(id=group_id)
            return Message.objects.create(sender=sender, group=group, content=content)
        except ChatGroup.DoesNotExist:
            return None
