from ninja import Schema
from typing import Optional, Literal


class ErrorSchema(Schema):
    message: str


class AccountRegistrationSchema(Schema):
    phone_number: str
    first_name: str
    last_name: str
    password: str
    code: str


class UsersMeSchema(Schema):
    avatar: Optional[str]
    username: str
    name: str
    id: int

    def resolve_name(self, obj):
        print(obj.__dict__)
        return obj.name


class PhoneSchema(Schema):
    phone_number: str


class AccountUpdateSchema(Schema):
    first_name: Optional[str]
    last_name: Optional[str]


class DeviceInputSchema(Schema):
    registration_id: str
    name: str | None
    device_id: str | None
    type: Optional[Literal["android", "web", "ios"]]
    
