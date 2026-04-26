"""
Access-control decorators for the Elan admin dashboard and role-gated views.
"""

from functools import wraps

from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.template.loader import render_to_string


def admin_required(view_func):
    """Allow only authenticated users whose role is 'admin'."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"/login/?next={request.path}")
        if request.user.role != "admin":
            messages.error(request, "Access denied. Restricted to administrators.")
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return wrapper


def login_required_with_role(role):
    """Return a decorator that enforces authentication and a specific role."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f"/login/?next={request.path}")
            if request.user.role != role:
                html = render_to_string("403.html", request=request)
                return HttpResponseForbidden(html)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def pro_validated_required(view_func):
    """Allow only authenticated, validated professional accounts."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"/login/?next={request.path}")
        if not (request.user.is_pro() and request.user.is_validated):
            messages.warning(request, "Account pending validation.")
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return wrapper
