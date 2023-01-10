import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path

from backend.api.consumer import GameConsumer, MessageConsumer, \
    AcceptanceLogEntryCreatedConsumer, LevelJoinLeftConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.prod')

"""
The code defines three consumers: GameConsumer, MessageConsumer, 
and AcceptanceLogEntryCreatedConsumer. 
These consumers are responsible for handling WebSocket requests for 
specific URLs: '/lobby_games/', '/msg/', and '/acceptanceLogEntryCreated/', 
respectively. The consumers are added to the URLRouter instance using the path 
function and the as_asgi method.
"""

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter([
                    path('lobby_games/', GameConsumer().as_asgi()),
                    path('msg/', MessageConsumer().as_asgi()),
                    path('acceptanceLogEntryCreated/',
                         AcceptanceLogEntryCreatedConsumer.as_asgi()),
                    path('joinLeft/', LevelJoinLeftConsumer().as_asgi()),

                ])
            )
        ),
    }
)
