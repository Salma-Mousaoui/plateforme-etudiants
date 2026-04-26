"""URL patterns for the chat app."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="chat"),
]
