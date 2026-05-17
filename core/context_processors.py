def navbar_context(request):
    current_page = None
    if hasattr(request, 'resolver_match') and request.resolver_match:
        current_page = request.resolver_match.url_name

    is_auth_page = current_page in ('login', 'register', 'password_reset')

    user_role = None
    if request.user.is_authenticated:
        user_role = getattr(request.user, 'role', None)

    return {
        'current_page': current_page,
        'is_auth_page': is_auth_page,
        'user_role': user_role,
    }
