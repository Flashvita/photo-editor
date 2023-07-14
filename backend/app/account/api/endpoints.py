from ninja import Router, File, UploadedFile
from ninja_jwt.authentication import JWTAuth

from django.core.cache import cache
from django.conf import settings

from fcm_django.models import FCMDevice

from commons.utils.phone_number import (
    validate_phone_number
)
from account.api.schemas import (
    AccountRegistrationSchema,
    ErrorSchema,
    UsersMeSchema,
    PhoneSchema,
    AccountUpdateSchema,
    DeviceInputSchema
)

from account.models import User
from account.api.services import (
    generate_code,
    verify_input_code,
    create_token,
    update_user_account
)



router = Router()


@router.post("register", response={200: dict,  400: ErrorSchema})
def register_account(request, payload: AccountRegistrationSchema):
    """
    Registration user with code from send-sms
    # api/v1/send-sms
    
    """
    try:
        print('payload')
        if not verify_input_code(payload.phone_number, payload.code):
            raise Exception("Invalid input code")
        user = User.objects.create(
            phone_number=payload.phone_number,
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


@router.post("send-sms", response={200: str ,  400: ErrorSchema})
def send_sms(request, payload: PhoneSchema):

    """Handler for send-sms by any actions
    """
    try:
        if validate_phone_number(payload.phone_number):
            code = generate_code()
            cache.set(
                            f"{payload.phone_number}-verify-code",
                            code,
                            settings.VERIFY_CODE_TIMEOUT
                    )
            return 200, code
        
    except Exception as e:
        print("Exception:", e)
        return 400,  {"message": f"{e}"}


@router.post(
        "/edit",
        auth=JWTAuth(),
        response={200: UsersMeSchema, 400: ErrorSchema}
)
def account_update(
    request,
    payload: AccountUpdateSchema = None,
    photo: UploadedFile = File(None)
):
    
    try:
        print('photo', photo)
        if payload is None:
            payload = AccountUpdateSchema(None)
        user = update_user_account(request.user, payload, photo)
        return 200, user
    except Exception as e:
        print("Exception:", e)
        return 400,  {"message": f"{e}"}

@router.get("/users-me",
            auth=JWTAuth(),
            response={200: UsersMeSchema,  400: ErrorSchema})
def get_user_info(request):
    """
    User detail information by firs request in login by set to client storage app
    """
    user = request.user
    return UsersMeSchema(
                         #phone_number=user.phone_number,
                         username=user.username,
                         name=user.name,
                         avatar=user.photo_link,
                         id=user.id
                        )


@router.post("/device", auth=JWTAuth())
def user_device(request, payload: DeviceInputSchema):
    """Creating or updating user device data 
    
        Request data :

                        {
                        "registration_id": "1wer2342fd534gfh67",    # обязательно - это токен FCM
                        "name": "Sony x5 v.11",                     # имя (необязательно) v-необходимо указывать для разделения названия устройства от версии ос 
                        "device_id": "24234123131",                 # id устройства (необязательно — может использоваться для уникальной идентификации устройств)
                        "type": "android"                           # тип ("android", "web", "ios")
                        }

        Response data:
                        status = 200
                        {
                        "success": true
                        }

        Raises :

                DataProcessingError:

                        status = 400
                        {
                        "message": "text error"
                        }


    """
    try:
        if fcm := FCMDevice.objects.filter(user_id=request.user).first():
            for key, value in payload.dict().items():
               if value == None:
                   continue
               setattr(fcm, key, value)
            fcm.save()
        else:
            FCMDevice.objects.create(**payload.dict(),  user=request.user)
        return {"success": True}
    except Exception as e:
        raise Exception(f"{e}")
