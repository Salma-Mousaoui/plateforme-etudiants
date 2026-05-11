"""URL patterns for the chat app."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="chat-list"),
    path("prive/<int:other_user_id>/", views.private_chat_view, name="chat-private"),
]
