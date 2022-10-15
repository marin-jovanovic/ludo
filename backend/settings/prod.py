""" Production Settings """

from .dev import *  # NOQA

DEBUG = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
MIDDLEWARE = [*MIDDLEWARE,
              'django.middleware.security.SecurityMiddleware']
SECURE_HSTS_SECONDS = 1
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_PRELOAD = True
