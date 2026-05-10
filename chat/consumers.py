import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import Message

User = get_user_model()


class PrivateChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        other_user_id = self.scope["url_route"]["kwargs"]["other_user_id"]
        u1 = min(user.id, int(other_user_id))
        u2 = max(user.id, int(other_user_id))
        self.room_name = f"chat_{u1}_{u2}"

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

        # Mark all unread messages from the other user as read on connect
        await self.mark_messages_read()

    async def disconnect(self, close_code):
        if hasattr(self, "room_name"):
            await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope["user"]
        other_user_id = int(self.scope["url_route"]["kwargs"]["other_user_id"])

        msg = await self.save_message(user, other_user_id, data["message"])
        if msg is None:
            return

        await self.channel_layer.group_send(self.room_name, {
            "type": "chat_message",
            "message": data["message"],
            "sender_id": user.id,
            "sender_name": user.get_full_name() or user.username,
            "sent_at": msg.sent_at.isoformat(),
            "is_read": False,
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, sender, receiver_id, content):
        try:
            receiver = User.objects.get(id=receiver_id)
            return Message.objects.create(sender=sender, receiver=receiver, content=content)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def mark_messages_read(self):
        user = self.scope["user"]
        other_user_id = int(self.scope["url_route"]["kwargs"]["other_user_id"])
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

        self.group_id = self.scope["url_route"]["kwargs"]["group_id"]
        self.room_name = f"chat_groupe_{self.group_id}"

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_name"):
            await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope["user"]

        await self.channel_layer.group_send(self.room_name, {
            "type": "chat_message",
            "message": data["message"],
            "sender_id": user.id,
            "sender": user.get_full_name() or user.username,
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
