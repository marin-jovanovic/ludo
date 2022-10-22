import os
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from backend.api.consumer import  Consumer, GameConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from backend.api.model.game import games_notifier

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.prod')


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter([
                    path('whole1/', GameConsumer().as_asgi())
                    # path('whole1/', PracticeConsumer().as_asgi())
                ])
            )
        ),
    }
)
