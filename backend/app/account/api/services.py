from django.conf import settings
from django.core.cache import cache

from ninja_jwt.tokens import RefreshToken

from account.models import User

import random
import string

def create_token(user):

    refresh = RefreshToken.for_user(user)
    return {
                "refresh": f"{refresh}",
                "access": f"{refresh.access_token}",
            }


def generate_code(digits_count: int = settings.ACCOUNT_VERIFICATION_CODE_DIGITS_COUNT):
    """Generate a random code for the given number of digits""" 
    return "".join(
        random.SystemRandom().choice(string.digits) for _ in range(digits_count)
    )

def verify_input_code(phone_number: str, code: str):
    print('code', code)
    print( 'cache code', cache.get(f"{phone_number}-verify-code"))
    return code == cache.get(f"{phone_number}-verify-code")
from typing import Optional

def update_user_account(user: User, data: Optional[dict], photo) -> User:
    print('data', data)
    update_fields = []
    if data:
        for attr, value in data.dict().items():
            print('attr', attr)
            print('value', value)
            if value != None:
                print(value)
                update_fields.append(attr)
            if  value == None:
                continue
            setattr(user, attr, value)
        user.save(update_fields=update_fields)
    if photo:
        user.avatar = photo
        user.save(update_fields=["avatar"])
    return user
