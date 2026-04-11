"""
Views for the reports app.
"""

from django.shortcuts import render  # noqa: F401


def index(request):
    """Page d'accueil de l'app reports."""
    return render(request, 'reports/index.html')
