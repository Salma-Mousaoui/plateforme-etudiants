"""
Views for the professionals app.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """Professionals listing page — requires authentication."""
    return render(request, 'professionals/index.html')
