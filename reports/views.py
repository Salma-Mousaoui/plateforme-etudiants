"""
Views for the reports app.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """Reports page — requires authentication."""
    return render(request, 'reports/index.html')
