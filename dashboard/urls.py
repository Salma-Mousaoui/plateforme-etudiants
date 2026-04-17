"""URL patterns for the dashboard app."""

from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    # Placeholder — replace with real DashboardView once built.
    path("", RedirectView.as_view(url="/", permanent=False), name="dashboard"),
]
