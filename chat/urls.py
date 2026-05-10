from django.urls import path
from . import views

urlpatterns = [
    path("", views.ChatListView, name="chat-list"),
    path("prive/<int:other_user_id>/", views.PrivateChatView, name="private-chat"),
    path("groupe/<int:group_id>/", views.GroupChatView, name="group-chat"),
]
