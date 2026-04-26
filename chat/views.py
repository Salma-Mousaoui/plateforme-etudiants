"""
Views for the chat app.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """Community chat page — requires authentication."""
    return render(request, 'chat/index.html')
