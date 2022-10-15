MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",

    # "backend.api.middleware.ipCheckMiddleware.IpCheckMiddleware",
    # "backend.api.middleware.bodyCheckMiddleware.BodyCheckMiddleware",
    # "backend.api.middleware.httpsCheckMiddleware.HttpsCheckMiddleware",
    # "backend.api.middleware.loginMiddleware.LoginMiddleware",
    # "backend.api.middleware.authCheckMiddleware.AuthCheckMiddleware",
    # "backend.api.middleware.roleCheckMiddleware.RoleCheckMiddleware",
    # "backend.api.middleware.msgBodyCheckMiddleware.MsgBodyCheckMiddleware",
    # "backend.api.middleware.CSRFCheckMiddleware.CSRFCheckMiddleware",

    "backend.api.middleware.jumperMiddleware.JumperMiddleware",

    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

"""
https://docs.djangoproject.com/en/2.1/ref/settings/
http://whitenoise.evans.io/en/stable/django.html?highlight=django

"""

import os

from decouple import config

SETTINGS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SETTINGS_DIR)

SECRET_KEY = config("SECRET_KEY")


DEBUG = True
ALLOWED_HOSTS = ['localhost']

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.sites',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'rest_framework',
    'backend.api',
    'django_extensions'
]

PWD = os.path.dirname(os.path.realpath(__file__))



CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['dist'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

_validation_path = 'django.contrib.auth.password_validation.'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': _validation_path + '.UserAttributeSimilarityValidator'},
    {'NAME': _validation_path + 'MinimumLengthValidator'},
    {'NAME': _validation_path + 'CommonPasswordValidator'},
    {'NAME': _validation_path + '.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MIDDLEWARE_CLASSES = (
    'whitenoise.middleware.WhiteNoiseMiddleware',
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'dist', 'static')
STATICFILES_DIRS = []

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# AUTH_USER_MODEL = 'backend.api.authentication_backends.user.User'
AUTHENTICATION_BACKENDS = [
    "backend.api.authentication_backends.keycloakBackend.KeycloakBackend",

    # 'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
    # 'social_core.backends.keycloak.KeycloakOAuth2',
    # 'django.contrib.auth.backends.ModelBackend'
]

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': config("DB_HOST"),
        'PORT': config("DB_PORT"),

    }
}