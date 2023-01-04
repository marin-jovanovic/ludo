import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path

from backend.api.consumer import GameConsumer, MessageConsumer, \
    AcceptanceLogEntryCreatedConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.prod')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter([
                    path('lobby_games/', GameConsumer().as_asgi()),
                    path('msg/', MessageConsumer().as_asgi()),
                    path('acceptanceLogEntryCreated/',
                         AcceptanceLogEntryCreatedConsumer.as_asgi())

                    # path('game_state/', MessageConsumer().as_asgi()),

                ])
            )
        ),
    }
)
