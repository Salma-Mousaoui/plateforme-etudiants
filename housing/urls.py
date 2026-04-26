"""URL patterns for the housing app."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="housing"),
]
