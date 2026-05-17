"""
Django settings for plateforme_etudiants project.
Python 3.11, Django 6.x, PostgreSQL (Supabase), Redis, Django Channels 4.x
"""

import os
from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# SECURITY
# ==============================================================================

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['*']

# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'channels',
    'storages',

    # Local apps
    'core',
    'housing',
    'professionals',
    'chat',
    'reports',
    'dashboard',
]

# ==============================================================================
# MIDDLEWARE
# ==============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.navbar_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# ==============================================================================
# DATABASE (PostgreSQL via Supabase)
# ==============================================================================

DATABASES = {
    'default': dj_database_url.parse(config('DATABASE_URL'))
}

# ==============================================================================
# CUSTOM USER MODEL
# ==============================================================================

AUTH_USER_MODEL = 'core.User'

# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = False

USE_TZ = True

# ==============================================================================
# STATIC FILES
# ==============================================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ==============================================================================
# MEDIA FILES (Uploads)
# ==============================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================================================================
# DJANGO CHANNELS
# InMemoryChannelLayer for development (single process, no Redis required).
# Switch to RedisChannelLayer before deploying to production.
# ==============================================================================

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# ==============================================================================
# AUTHENTICATION
# ==============================================================================

LOGIN_URL           = '/login/'
# CustomLoginView.get_success_url() overrides this with role-based routing
LOGIN_REDIRECT_URL  = '/dashboard/etudiant/'
LOGOUT_REDIRECT_URL = '/'

# Authentification par email au lieu de username
AUTHENTICATION_BACKENDS = [
    'core.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Map the ERROR level tag to 'danger' so CSS class elan-toast-danger applies
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {message_constants.ERROR: 'danger'}

# ==============================================================================
# DEFAULT AUTO FIELD
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# SUPABASE STORAGE (django-storages + boto3 S3 backend)
# Set USE_SUPABASE_STORAGE=True in .env to enable cloud storage.
# ==============================================================================

USE_SUPABASE_STORAGE = config('USE_SUPABASE_STORAGE', default=False, cast=bool)

if USE_SUPABASE_STORAGE:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_ENDPOINT_URL = config('SUPABASE_S3_ENDPOINT')
    AWS_ACCESS_KEY_ID = config('SUPABASE_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = config('SUPABASE_SECRET_KEY')
    AWS_STORAGE_BUCKET_NAME = 'profiles'
    AWS_S3_REGION_NAME = config('SUPABASE_REGION', default='eu-west-1')
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = 'public-read'
    AWS_QUERYSTRING_AUTH = False
    SUPABASE_URL = config('SUPABASE_URL')
    MEDIA_URL = f"{SUPABASE_URL}/storage/v1/object/public/"
else:
    if not globals().get('MEDIA_URL'):
        MEDIA_URL = '/media/'
        MEDIA_ROOT = BASE_DIR / 'media'
