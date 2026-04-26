"""URL patterns for the reports app."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="reports"),
]
