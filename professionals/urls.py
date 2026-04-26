"""URL patterns for the professionals app."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="professionals"),
]
