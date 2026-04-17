"""URL patterns for the core app."""

from django.urls import path
from django.views.generic import RedirectView

from .views import LandingView

urlpatterns = [
    path("", LandingView.as_view(), name="landing"),

    # Placeholder URL names required by base.html navbar.
    # Replace each RedirectView with its real view once built.
    path("register/", RedirectView.as_view(url="/", permanent=False), name="register"),
    path("profil/",   RedirectView.as_view(url="/", permanent=False), name="profil"),
]
