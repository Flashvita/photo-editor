
import flet as ft

import requests
import json

from app_settings.settings import CORS_ORIGIN
from account import Login, Registration
from flet import (
   
    View,
   
)


def navbar():
    navbar = ft.NavigationBar(
                        elevation=30,
                        bgcolor=ft.colors.LIGHT_BLUE_200,
                        label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_HIDE, # Dont work hide label behavior for navigate
                        selected_index=5,
                        destinations=[
                            ft.NavigationDestination(icon=ft.icons.HOME, label="Главная"),
                            ft.NavigationDestination(icon=ft.icons.SEARCH_SHARP, label="Поиск"),
                            ft.NavigationDestination(icon=ft.icons.ADD_A_PHOTO_OUTLINED, label="Добавить фото"),
                            ft.NavigationDestination(
                                icon=ft.icons.CIRCLE_NOTIFICATIONS,
                                label="Уведомления",
                            ),
                            ft.NavigationDestination(
                                icon=ft.icons.FAVORITE,
                                label="Избранное",
                            ), 
                            
                        ]
                    )
    return navbar


def appbar(data, func):
    appbar = ft.AppBar(
                        leading=ft.Icon(ft.icons.PALETTE),
                        leading_width=40,
                        title=ft.Text("Photoeditor"),
                        center_title=True,
                        bgcolor=ft.colors.LIGHT_BLUE_200,
                        actions=[
                                    ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE_SHARP, on_click=func),
                                ],
                        )
    return appbar


def appbar_profile(data, func):
    appbar  = ft.AppBar(
                        elevation=5,
                        leading=ft.Icon(ft.icons.PALETTE),
                        leading_width=40,
                        #title=ft.Text(f"{data['name']}"),
                        title=ft.Text(f"Анна Кулешова"),

                        center_title=True,
                        bgcolor=ft.colors.LIGHT_BLUE_200,
                        actions=[
                            
                                ft.IconButton(icon=ft.icons.SETTINGS, on_click=func),
                                
                            ],
                        )
    return appbar


                    #controls = [favorites]
def profile(obj):
    obj.page.go("/dashboard/profile")

def logout(obj):
    obj.page.go("/logout")

def profile_settings(obj):
    obj.page.go("/dashboard/profile/settings")


def routes(obj):
    page = obj.page
    print("Route change:", obj.route)
    
    #print('token', page.client_storage.get("access_token"))
    if token := page.client_storage.get("access_token") and page.route == "/":
        print('go dashboard')
        page.go("/dashboard")
    else:
        login = Login(page)
        page.views.append(
            View(
                "/",
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                vertical_alignment = ft.MainAxisAlignment.CENTER,
                controls = [login],
                )
        )
    if page.route == "/registration":
        page.views.clear()
        registration = Registration(page)
        page.views.append(
            View(
                "/registration",
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                vertical_alignment = ft.MainAxisAlignment.CENTER,
                controls = [registration],
                )
        )
    if page.route == "/logout":
        page.client_storage.remove(key="access_token")
        page.go("/")
    if page.route == "/dashboard/profile":
        #favorites = Profile(page)
        data = page.client_storage.get("user_data")
        print('go profile')
        page.views.append(
            View(
            "/dashboard/profile",
            appbar=appbar_profile(data, profile_settings),
            navigation_bar=navbar(),
            padding=0,
            controls= [
                 ft.Row(
            [
                ft.Container(
                    content=ft.Image(
                        src=f"assert/icons/test1.jpg",
                        width=150,
                        height=200,
                        fit=ft.ImageFit.COVER,
                        border_radius=ft.border_radius.all(15),
                ),
                    expand=2,
                    margin=2,
                    padding=2,
                    alignment=ft.alignment.top_left,
                    width=150,
                    height=200,
                    border_radius=10,
                ),
                
                ft.Container(
                    content=ft.Text(
                       "10 подписок",
                       font_family="Verdana" 
                       #You can use font_family "Consolas", "Arial", "Verdana", "Tahoma"
                ),
                    margin=10,
                    padding=10,
          
                    expand=1,
                    border_radius=10,
                ),
                
                
            ],
            alignment=ft.MainAxisAlignment.START,
        ),

            ft.Container(
            content=ft.NavigationBar(
                        elevation=30,
                        bgcolor=ft.colors.YELLOW_50,
                        label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_HIDE, # Dont work hide label behavior for navigate
                        selected_index=5,
                        destinations=[
                            ft.NavigationDestination(icon=ft.icons.VIDEO_FILE_OUTLINED, label="Добавить видео"),
                            ft.NavigationDestination(
                                icon=ft.icons.PICTURE_IN_PICTURE,
                                label="Картина",
                            ),
                            ft.NavigationDestination(
                                icon=ft.icons.PHOTO_ALBUM_ROUNDED,
                                label="Фото альбом",
                            ), 
                            
                        ]
                    )
            )
            ]
            )
        )
    if page.route == "/dashboard/profile/settings":
        #favorites = Profile(page)
        data = page.client_storage.get("user_data")
        print('go profile')
        page.views.append(
            View(
                    "/dashboard/profile/settings",
                    controls=[ft.ElevatedButton(text="Logout", on_click=logout)]
                )
        )
                
    if page.route == "/dashboard":
                
        #dashboard = Dashboard(page)
        #page.clean()
        token = page.client_storage.get("access_token")
        headers = {
                    "Authorization": f"Bearer {token}"
                }
        url = f"{CORS_ORIGIN}api/v1/account/users-me"
        response = requests.get(url, headers=headers)
        data = json.loads(response.content)
        page.client_storage.set("user_data", data)
        page.views.append(
            View(
                "/dashboard",
                appbar=appbar(data, profile),
                navigation_bar = navbar()
                    # controls = [
                    #             dashboard
                    #         ],
                        )
                    )
    page.update()