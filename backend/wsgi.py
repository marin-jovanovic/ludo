"""
WSGI config for project project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import time
from threading import Thread

from django.core.wsgi import get_wsgi_application

# This will set production as default, but we must still set it with an
# ENV on heroku to ensure that the migrate command runs agains the correct DB
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.prod')

print("wsgi")
print(80 * "-")
application = get_wsgi_application()

from backend.api.ws.main import init_server

def task():
    print("task")
    init_server()
    # block for a moment
    # time.sleep(15)
    # sleep(1)
    # display a message
    print('This is from another thread')
    # users = get_logged_users()
    # users = await database_sync_to_async(get_logged_users())()

    # print(f"{users=}")


thread = Thread(target=task)
thread.start()

#
# init_server()
# print("after")