from app_settings.settings import (
    CORS_ORIGIN,
    SECRET_KEY,
)

import flet as ft
# from account import (
#     Login,
#     Registration,
#     SendSms,
#     account_routes
# )

from flet.security import encrypt, decrypt

_secret_key = SECRET_KEY


# def navbar():
#     navbar = ft.NavigationBar(
#                         elevation=30,
#                         bgcolor=ft.colors.LIGHT_BLUE_200,
#                         label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_HIDE, # Dont work hide label behavior for navigate
#                         selected_index=5,
#                         destinations=[
#                             ft.NavigationDestination(icon=ft.icons.HOME, label="Главная"),
#                             ft.NavigationDestination(icon=ft.icons.SEARCH_SHARP, label="Поиск"),
#                             ft.NavigationDestination(icon=ft.icons.ADD_A_PHOTO_OUTLINED, label="Добавить фото"),
#                             ft.NavigationDestination(
#                                 icon=ft.icons.CIRCLE_NOTIFICATIONS,
#                                 label="Уведомления",
#                             ),
#                             ft.NavigationDestination(
#                                 icon=ft.icons.FAVORITE,
#                                 label="Избранное",
#                             ), 
                            
#                         ]
#                     )
#     return navbar


# def appbar(data, func):
#     appbar = ft.AppBar(
#                         leading=ft.Icon(ft.icons.PALETTE),
#                         leading_width=40,
#                         title=ft.Text("Photoeditor"),
#                         center_title=True,
#                         bgcolor=ft.colors.LIGHT_BLUE_200,
#                         actions=[
#                                     ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE_SHARP, on_click=func),
#                                 ],
#                         )
#     return appbar


# def appbar_profile(data, func):
#     appbar  = ft.AppBar(
#                         elevation=5,
#                         leading=ft.Icon(ft.icons.PALETTE),
#                         leading_width=40,
#                         #title=ft.Text(f"{data['name']}"),
#                         title=ft.Text(f"Анна Кулешова"),

#                         center_title=True,
#                         bgcolor=ft.colors.LIGHT_BLUE_200,
#                         actions=[
                            
#                                 ft.IconButton(icon=ft.icons.SETTINGS, on_click=func),
                                
#                             ],
#                         )
#     return appbar

# def encrypt_value(key: str):
#     #https://flet.dev/docs/guides/python/encrypting-sensitive-data/
#     secret = encrypt(key, _secret_key)
#     return secret


# def decrypt_value(key: str):
#     #https://flet.dev/docs/guides/python/encrypting-sensitive-data/
#     secret = decrypt(key, _secret_key)
#     return secret


# def profile(obj):
#     obj.page.go("/dashboard/profile")

# def logout(obj):
#     obj.page.go("/logout")

# def profile_settings(obj):
#     obj.page.go("/dashboard/profile/settings")

# def user_auth(page):
#     token = page.client_storage.get("access_token")
#     print('token', token)
#     if token and page.route == "/":
#         print('go dashboard')
#         page.go("/dashboard")
#     else:
#         login = Login(page)
#         page.views.append(
#             View(
#                 "/account",
#                 horizontal_alignment = ft.CrossAxisAlignment.CENTER,
#                 vertical_alignment = ft.MainAxisAlignment.CENTER,
#                 controls = [login],
#                 )
#         )
# def routes(obj):
#     page = obj.page
#     print("Route change:", obj.route)
#     user_auth(page)
#     print("Route after user_auth:", obj.route)
#     if page.route.startswith("/account"):
#         print("startswith account")
#     #print('token', page.client_storage.get("access_token"))
#         account_routes(obj)
#     if page.route.startswith("/dashboard"):
#         dashboard_router(obj)
#     page.update()