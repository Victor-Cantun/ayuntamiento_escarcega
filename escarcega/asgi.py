"""
ASGI config for escarcega project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "escarcega.settings")

application = get_asgi_application()

# from a_chat.routing import websocket_urlpatterns as chat_websocket
##from a_notifications.routing import webcsoket_urlpatterns as notifications_websocket

# websocket_urlpatterns = chat_websocket + notifications_websocket
from apps.a_notifications import routing

application = ProtocolTypeRouter(
    {
        "http": application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
        ),
    }
)
