from flet import View, CrossAxisAlignment, MainAxisAlignment

from .controls import Registration, SendSms
from .services import user_check_auth


def routes(obj):
    page = obj.page
    print("Account route:", obj.route)
    user_check_auth(page)
    # print('token', page.client_storage.get("access_token"))
    if page.route == "/account/registration":
        page.views.clear()
        # registration = Registration(page)
        page.views.append(
            View(
                "/account/registration",
                horizontal_alignment=CrossAxisAlignment.CENTER,
                vertical_alignment=MainAxisAlignment.CENTER,
                controls=[Registration(page)],
                )
        )
    if page.route == "/account/logout":
        page.client_storage.remove(key="access_token")
        page.go("/account")
    if page.route == "/account/recover-password":
        page.views.append(
            View(
                "/account/recover-password",
                horizontal_alignment=CrossAxisAlignment.CENTER,
                vertical_alignment=MainAxisAlignment.CENTER,
                controls=[
                    SendSms(page)
                    ]
            ))


#from flet.security import encrypt, decrypt



# def encrypt_value(key: str):
#     #https://flet.dev/docs/guides/python/encrypting-sensitive-data/
#     secret = encrypt(key, _secret_key)
#     return secret


# def decrypt_value(key: str):
#     #https://flet.dev/docs/guides/python/encrypting-sensitive-data/
#     secret = decrypt(key, _secret_key)
#     return secret
