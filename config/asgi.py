import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# get_asgi_application() calls django.setup() — must happen before any
# import that touches models or settings (channels, chat.routing, etc.).
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import chat.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # AllowedHostsOriginValidator rejects WS upgrade requests whose
    # Origin header doesn't match ALLOWED_HOSTS, preventing cross-site
    # WebSocket hijacking and giving a clear error when the host isn't
    # configured rather than a silent handshake failure.
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(chat.routing.websocket_urlpatterns)
        )
    ),
})
