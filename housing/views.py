"""
Views for the housing app.
"""

from django.shortcuts import render  # noqa: F401


def index(request):
    """Page d'accueil de l'app housing."""
    return render(request, 'housing/index.html')
