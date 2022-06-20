import os
from . base import *
from dotenv import load_dotenv
from datetime import timedelta

# Loading env values from .env file
load_dotenv()

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Frontend BASE URL
FRONTEND_BASE_URL = 'http://localhost:3000/'

# Databases Config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('PG_NAME', 'cleanform_development'),
        'USER': os.environ.get('PG_USER', 'cleanform'),
        'PASSWORD': os.environ.get('PG_PASSWORD', 'cleanform'),
        'HOST': os.environ.get('PG_HOST', 'localhost'),
        'PORT': os.environ.get('PG_PORT', '5432'),
    },
    'replica1': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('PG_REPLICA1_NAME', 'cleanform_development_replica1'),
        'USER': os.environ.get('PG_REPLICA1_USER', 'cleanform'),
        'PASSWORD': os.environ.get('PG_REPLICA1_PASSWORD', 'cleanform'),
        'HOST': os.environ.get('PG_REPLICA1_HOST', 'localhost'),
        'PORT': os.environ.get('PG_REPLICA1_PORT', '5433'),
    },
    'replica2': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('PG_REPLICA1_NAME', 'cleanform_development_replica2'),
        'USER': os.environ.get('PG_REPLICA1_USER', 'cleanform'),
        'PASSWORD': os.environ.get('PG_REPLICA1_PASSWORD', 'cleanform'),
        'HOST': os.environ.get('PG_REPLICA1_HOST', 'localhost'),
        'PORT': os.environ.get('PG_REPLICA1_PORT', '5434'),
    },
}

# Database Routing Config
DATABASE_ROUTERS = ['app.db_routers.PrimaryReplicaRouter']

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

# JWT Config
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# CORS Setup
CORS_ALLOW_ALL_ORIGINS = True

# Email
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'log/emails'
DEFAULT_FROM_EMAIL = 'Cleanform <noreply@cleanform.io>'

# Logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR / 'log/debug.log',
#         },
#     },
#     'loggers': {
#         'rest_framework.request': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
