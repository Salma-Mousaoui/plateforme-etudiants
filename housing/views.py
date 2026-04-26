"""
Views for the housing app.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """Housing listings page — requires authentication."""
    return render(request, 'housing/index.html')
