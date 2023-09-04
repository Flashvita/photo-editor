import random
import string

from django.conf import settings
from django.core.cache import cache

from ninja_jwt.tokens import RefreshToken

from account.models import User

from typing import Optional


def create_token(user):
    """
    Custom create token data without request api
    """

    refresh = RefreshToken.for_user(user)
    return {
                "refresh": f"{refresh}",
                "access": f"{refresh.access_token}",
            }


def generate_code(
        digits_count: int = settings.ACCOUNT_VERIFICATION_CODE_DIGITS_COUNT
):
    """Generate a random code for the given number of digits""" 
    return "".join(
        random.SystemRandom().choice(string.digits) for _ in range(digits_count)
    )


def verify_input_code(phone_number: str, code: str):
    return code == cache.get(f"{phone_number}-verify-code")


def update_user_account(user: User, data: Optional[dict], photo) -> User:
    update_fields = []
    if data:
        for attr, value in data.dict().items():
            if value != None:
                print(value)
                update_fields.append(attr)
            if value is None:
                continue
            setattr(user, attr, value)
        user.save(update_fields=update_fields)
    if photo:
        user.avatar = photo
        user.save(update_fields=["avatar"])
    return user
