from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/prive/(?P<other_user_id>\d+)/$", consumers.PrivateChatConsumer.as_asgi()),
    re_path(r"ws/chat/groupe/(?P<group_id>\d+)/$", consumers.GroupChatConsumer.as_asgi()),
]
