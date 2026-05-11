"""
WebSocket consumers for the chat app.
Private 1-to-1 chat and group chat.
"""

import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model


@database_sync_to_async
def _save_private_message(sender_id, receiver_id, content):
    from .models import Message
    User = get_user_model()
    sender   = User.objects.get(pk=sender_id)
    receiver = User.objects.get(pk=receiver_id)
    return Message.objects.create(sender=sender, receiver=receiver, content=content)


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for private 1-to-1 chat."""

    async def connect(self):
        self.room_name       = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_prive_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data        = json.loads(text_data)
        message     = data['message']
        sender      = data.get('sender', 'Unknown')
        sender_id   = data.get('sender_id')
        receiver_id = data.get('receiver_id')

        if sender_id and receiver_id and message.strip():
            await _save_private_message(sender_id, receiver_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':      'chat_message',
                'message':   message,
                'sender':    sender,
                'sender_id': sender_id,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message':   event['message'],
            'sender':    event['sender'],
            'sender_id': event.get('sender_id'),
        }))


class GroupChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for group chat."""

    async def connect(self):
        self.group_name      = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = f'chat_groupe_{self.group_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data    = json.loads(text_data)
        message = data['message']
        sender  = data.get('sender', 'Unknown')
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message': message, 'sender': sender}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender':  event['sender'],
        }))
