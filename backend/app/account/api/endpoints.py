from ninja import Router

from ninja_jwt.authentication import JWTAuth
from account.api.schemas import (
    AccountRegistrationSchema,
    ErrorSchema,
    UsersMeSchema,
    PhoneSchema
)
from django.contrib.auth import get_user_model
from account.api.services import (
    generate_code,
    verify_input_code,
    create_token
)
from django.core.cache import cache
from django.conf import settings

User = get_user_model()

router = Router()


@router.post("register", response={200: dict,  400: ErrorSchema})
def test_api(request, payload: AccountRegistrationSchema):
    try:
        print('payload')
        if not verify_input_code(payload.username, payload.code):
            raise Exception("Invalid input code")
        user = User.objects.create(
            username=payload.username,
            first_name=payload.first_name,
            last_name=payload.last_name,
        )
        user.set_password(payload.password)
        user.save(update_fields=["password"])
        token = create_token(user)
        print('new user token', token)
        return 200,  token
    except Exception as e:
        print("Exception by registration", e)
        return 400,  {"message": f"{e}"}


@router.post("send-sms", response={200: str,  400: ErrorSchema})
def send_sms(request, payload: PhoneSchema):

    """Отправка смс для регистрации и сброса пароля
    """
    try:
        code = generate_code()
        print("code", code)
        cache.set(
                        f"{payload.phone_number}-verify-code",
                        code,
                        settings.VERIFY_CODE_TIMEOUT
                )
        return 200, code

    except Exception as e:
        print("Exception:", e)
        raise Exception(f"{e}")

@router.get('test')
def test(request):
    return 200, "hello world"


@router.get("/users-me",
            auth=JWTAuth(),
            response={200: UsersMeSchema,  400: ErrorSchema})
def get_user_info(request):
    user = request.user
    return UsersMeSchema(
                         phone_number = user.username,
                         name = f"{user.first_name} {user.last_name}",
                         id=user.id
                         )
