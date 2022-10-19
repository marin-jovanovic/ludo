"""
WSGI config for project project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import time
from threading import Thread

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.wsgi import get_wsgi_application

# This will set production as default, but we must still set it with an
# ENV on heroku to ensure that the migrate command runs agains the correct DB
from django.urls import path

from backend.api.consumer import PracticeConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.prod')

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

print("wsgi")
# print(80 * "-")
application = get_wsgi_application()

# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(
#                 URLRouter([
#                     path('whole1/', PracticeConsumer().as_asgi())
#                     # re_path(r"^front(end)/$",
#                     #         consumers.AsyncChatConsumer.as_asgi()),
#                 ])
#             )
#         ),
#         # Just HTTP for now. (We can add other protocols later.)
#     }
# )
#
# from backend.api.ws.main import init_server
#
# def task():
#     print("task")
#     init_server()
#     print('This is from another thread')
#
#

# thread = Thread(target=task)
# thread.start()
