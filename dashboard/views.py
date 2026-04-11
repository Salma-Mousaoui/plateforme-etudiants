"""
Views for the dashboard app.
"""

from django.shortcuts import render  # noqa: F401


def index(request):
    """Page d'accueil de l'app dashboard."""
    return render(request, 'dashboard/index.html')
