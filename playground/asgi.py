import os

import django
# from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter,get_default_application

from django.conf import settings
settings.configure()

import django
django.setup()


import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

# from backend.api.consumer import PracticeConsumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from backend.api.consumer import PingConsumer
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.dev")
# django.setup()


# application=get_default_application()
# django.setup()
# ws_patterns = [
#
#     path('ws/a', PingConsumer.as_asgi())
# ]

from channels.routing import ProtocolTypeRouter, get_default_application


application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_default_application(),

    # WebSocket chat handler
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                # path("ws", PingConsumer.as_asgi()),
                path("/ws", PingConsumer.as_asgi()),
                # path("ws/", PingConsumer.as_asgi()),
                # path("/ws/", PingConsumer.as_asgi()),
                path("/", PingConsumer.as_asgi()),
                # path("", PingConsumer.as_asgi()),
            ])
        )
    ),
})

#
#
# import os
#
# from channels.routing import ProtocolTypeRouter
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.dev')
#
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     # Just HTTP for now. (We can add other protocols later.)
# })
#
#
# import os
#
# from backend.api.ws.ws_daphne import websocket_application
#
# async def application(scope, receive, send):
#         await websocket_application(scope, receive, send)