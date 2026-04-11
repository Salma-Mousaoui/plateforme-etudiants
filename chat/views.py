"""
Views for the chat app.
"""

from django.shortcuts import render  # noqa: F401


def index(request):
    """Page d'accueil de l'app chat."""
    return render(request, 'chat/index.html')
