"""
WebSocket URL routing for the chat app.
"""

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/prive/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/groupe/<str:group_name>/', consumers.GroupChatConsumer.as_asgi()),
]
