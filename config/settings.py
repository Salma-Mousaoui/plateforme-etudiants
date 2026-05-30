"""
Django settings for plateforme_etudiants project.
Python 3.11, Django 6.x, PostgreSQL (Supabase), Redis, Django Channels 4.x
"""

from pathlib import Path
from decouple import config
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# SECURITY
# ==============================================================================

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=lambda v: [s.strip() for s in v.split(',')],
)

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='',
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()],
)

# Railway reverse-proxy : indique à Django que le trafic entrant est HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Cookies sécurisés uniquement en production (HTTPS)
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

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

STORAGES = {
    "default": {
        # Production: Supabase S3-compatible storage (USE_SUPABASE_STORAGE=True)
        # Development: local filesystem (USE_SUPABASE_STORAGE=False or unset)
        "BACKEND": (
            'storages.backends.s3boto3.S3Boto3Storage'
            if config('USE_SUPABASE_STORAGE', default=False, cast=bool)
            else 'django.core.files.storage.FileSystemStorage'
        ),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ==============================================================================
# MEDIA FILES + SUPABASE STORAGE (S3-compatible)
# Dev  (USE_SUPABASE_STORAGE=False): FileSystemStorage → local MEDIA_ROOT
# Prod (USE_SUPABASE_STORAGE=True):  S3Boto3Storage    → Supabase bucket
# ==============================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

USE_SUPABASE_STORAGE = config('USE_SUPABASE_STORAGE', default=False, cast=bool)

if USE_SUPABASE_STORAGE:
    AWS_ACCESS_KEY_ID       = config('SUPABASE_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY   = config('SUPABASE_SERVICE_KEY')
    AWS_STORAGE_BUCKET_NAME = config('SUPABASE_BUCKET_NAME', default='media')
    AWS_S3_ENDPOINT_URL     = config('SUPABASE_S3_ENDPOINT')
    AWS_S3_REGION_NAME      = config('SUPABASE_REGION', default='eu-central-1')
    AWS_S3_FILE_OVERWRITE   = False
    AWS_DEFAULT_ACL         = 'public-read'
    AWS_QUERYSTRING_AUTH    = False
    MEDIA_URL = (
        f"{config('SUPABASE_URL')}/storage/v1/object/public/"
        f"{config('SUPABASE_BUCKET_NAME', default='media')}/"
    )
elif not DEBUG:
    raise ImproperlyConfigured(
        "USE_SUPABASE_STORAGE is not set to True in production. "
        "Set USE_SUPABASE_STORAGE=True in Railway → Variables."
    )

# ==============================================================================
# DJANGO CHANNELS
# ==============================================================================

_redis_url = config('REDIS_URL', default='')

if not DEBUG and not _redis_url:
    raise ImproperlyConfigured(
        "REDIS_URL environment variable is not set. "
        "Add it in Railway → Variables (copy from your Redis service → Connect tab)."
    )

# Local dev fallback when REDIS_URL is not in .env
if not _redis_url:
    _redis_url = 'redis://localhost:6379'

# Railway provides rediss:// (TLS). Pass ssl_cert_reqs=None to skip cert
# verification against Railway's self-signed cert.
_redis_host = (
    {"address": _redis_url, "ssl_cert_reqs": None}
    if _redis_url.startswith("rediss://")
    else _redis_url
)

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [_redis_host],
            # capacity: max messages queued per channel before back-pressure kicks in.
            # expiry: seconds before an unread message is dropped from the queue.
            # Both prevent Redis memory from growing unbounded if a consumer is slow.
            'capacity': 1500,
            'expiry': 10,
        },
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

