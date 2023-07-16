from datetime import timedelta
from urllib import parse
from pathlib import Path


import os
import environ

BASE_DIR = Path(__file__).resolve().parent

env = environ.Env()
environ.Env.read_env()

#environ.Env.read_env(os.path.join(BASE_DIR, '../.env'))

import os

print("BASE_DIR", BASE_DIR)
# Base url backend api
# CORS_ORIGIN = "http://127.0.0.1:8000/"
CORS_ORIGIN = env("CORS_ORIGIN")
SECRET_KEY = env("APP_SECRET_KEY")

#

# from flet.security import encrypt, decrypt

# secret_key = os.getenv("MY_APP_SECRET_KEY")
# plain_text = "This is a secret message!"
# encrypted_data = encrypt(plain_text, secret_key)