"""
Views for the core app.
"""

from django.shortcuts import render  # noqa: F401


def index(request):
    """Page d'accueil de l'app core."""
    return render(request, 'core/index.html')
