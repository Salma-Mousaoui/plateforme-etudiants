"""
Views for the professionals app.
"""

from django.shortcuts import render  # noqa: F401


def index(request):
    """Page d'accueil de l'app professionals."""
    return render(request, 'professionals/index.html')
