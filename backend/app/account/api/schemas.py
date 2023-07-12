from ninja import Schema


class ErrorSchema(Schema):
    message: str


class AccountRegistrationSchema(Schema):
    username: str
    first_name: str
    last_name: str
    password: str
    code: str
   
class UsersMeSchema(Schema):
    phone_number: str
    name: str
    id: int

class PhoneSchema(Schema):
    phone_number: str

