from datetime import timedelta
from urllib import parse
from pathlib import Path


import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('DJANGO_SECRET_KEY')
DJANGO_CONFIG = env('DJANGO_CONFIG')
CSRF_TRUSTED_ORIGINS = [
        env("CORS_ORIGIN"),
        
    ]


REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')

CACHES = {
    "default": {
        #"BACKEND": "commons.redis.cache.RedisCache", # Custom validators
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}',
        # "OPTIONS": {
        #     "CLIENT_CLASS": "django_redis.client.DefaultClient",
        # }
    }
}

DATABASES = {
    'default': {
        'ATOMIC_REQUESTS': False,
        'AUTOCOMMIT': True,
        'ENGINE': 'django.db.backends.postgresql', 
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': 5432,
        # 'OPTIONS': {},
        # 'TEST': {},
        # 'TIME_ZONE': None,

    }
}



NINJA_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    #'ROTATE_REFRESH_TOKENS': False,
    #'BLACKLIST_AFTER_ROTATION': False,
    #'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'ninja_jwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('ninja_jwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'ninja_jwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    #'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    #'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    #'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
