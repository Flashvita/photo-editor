from datetime import timedelta
from urllib import parse
from pathlib import Path


import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

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