
import requests
import json

from app_settings.settings import CORS_ORIGIN

from flet.security import encrypt, decrypt
from flet import (
    Container,
    Row,
    ElevatedButton,
    Image,
    ImageFit,
    Text,
    MainAxisAlignment,
    NavigationBar,
    NavigationBarLabelBehavior,
    NavigationDestination,
    View,
    alignment,
    border_radius, 
    icons,
    colors
)


from .services import appbar, appbar_profile, navbar

def profile(obj):
    obj.page.go("/dashboard/profile")

def logout(obj):
    obj.page.go("/account/logout")

def profile_settings(obj):
    obj.page.go("/dashboard/profile/settings")
    
def routes(obj):
    page = obj.page
    if page.route == "/dashboard/profile":
        #favorites = Profile(page)
        data = page.client_storage.get("user_data")
        print('go profile')
        page.views.append(
            View(
            "/dashboard/profile",
            appbar=appbar_profile(data, profile_settings),
            navigation_bar = navbar(),
            padding=0,
            controls= [
                Row(
            [
                Container(
                    content=Image(
                        src=f"assert/icons/test1.jpg",
                        width=150,
                        height=200,
                        fit=ImageFit.COVER,
                        border_radius=border_radius.all(15),
                ),
                    expand=2,
                    margin=2,
                    padding=2,
                    alignment=alignment.top_left,
                    width=150,
                    height=200,
                    border_radius=10,
                ),
                
                Container(
                    content=Text(
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
            alignment=MainAxisAlignment.START,
        ),

            Container(
            content=NavigationBar(
                        elevation=30,
                        bgcolor=colors.YELLOW_50,
                        label_behavior=NavigationBarLabelBehavior.ALWAYS_HIDE, # Dont work hide label behavior for navigate
                        selected_index=5,
                        destinations=[
                            NavigationDestination(icon=icons.VIDEO_FILE_OUTLINED, label="Добавить видео"),
                            NavigationDestination(
                                icon=icons.PICTURE_IN_PICTURE,
                                label="Картина",
                            ),
                            NavigationDestination(
                                icon=icons.PHOTO_ALBUM_ROUNDED,
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
                    controls=[ElevatedButton(text="Logout", on_click=logout)]
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
                navigation_bar = navbar(page)
                    # controls = [
                    #             dashboard
                    #         ],
                        )
                    )