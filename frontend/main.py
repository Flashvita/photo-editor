import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors
from app_settings.settings import CORS_ORIGIN
from flet import (
    UserControl,
    AppBar,
    ElevatedButton,
    Icon,
    IconButton,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    Row,
    Text,
    colors,
    icons,
    theme,
)

LIGHT_SEED_COLOR = colors.DEEP_ORANGE
DARK_SEED_COLOR = colors.INDIGO


from account import Registration, Login

from dashboard import Dashboard, DashboardAppBar

class PanelTools(UserControl):
    """Tools panel in navigate bar
    """

    def __init__(self, page):
        super().__init__()
        self.page = page


    def build(self):
        self.navbar_view = ft.Column(ft.NavigationBar(
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
        )
        return self.navbar_view

class Profile(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page


    def build(self):
        self.favorites_views = ft.Column(controls = [ft.Text(value="Profile settings")])
        return self.favorites_views

 
if __name__ == "__main__":
    def main(page: Page):
        page.title = "PhotoGraph"
        page.theme_mode = "light"
        page.theme = theme.Theme(color_scheme_seed=LIGHT_SEED_COLOR, use_material3=True)
        page.dark_theme = theme.Theme(color_scheme_seed=DARK_SEED_COLOR, use_material3=True)
        page.update()

        print("Initial route:", page.route)
        

        def profile_settings(e):
            page.go("dashboard/profile")

        def route_change(e):
            print("Route change:", e.route)
            page.views.clear()
            login = Login(page)
            print('token', page.client_storage.get("access_token"))
            if token := page.client_storage.get("access_token"):
                print('go dashboard')
                page.go("/dashboard")
            else:
                page.views.append(
                    View(
                        "/",
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                        vertical_alignment = ft.MainAxisAlignment.CENTER,
                        controls = [ 
                                    login
                                ],
                        )
                )
            if page.route == "/registration":
                registration = Registration(page)
                page.views.append(
                    View(
                    "/registration",
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    vertical_alignment = ft.MainAxisAlignment.CENTER,
                    controls = [ 
                                registration
                            ],
                    )
            )
            if page.route == "dashboard/profile":
                favorites = Profile(page)
                page.views.append(
                    View(
                    "/dashboard/profile",
                    controls = [favorites]
                )
                )
            if page.route == "/dashboard":
                import requests
                import json
                dashboard = Dashboard(page)
                page.clean()
                #app_bar = DashboardAppBar(page)
                #navigation_bar = PanelTools(page)
                token = page.client_storage.get("access_token")
                headers = {
                    "Authorization": f"Bearer {token}"
                }
                url = f"{CORS_ORIGIN}api/v1/account/users-me"
                response = requests.get(url, headers=headers)
                data = json.loads(response.content)

                page.views.append(
                    View(
                    "/dashboard",
                    appbar=ft.AppBar(
                        leading=ft.Icon(ft.icons.PALETTE),
                        leading_width=40,
                        title=ft.Text("Photographer"),
                        center_title=True,
                        bgcolor=ft.colors.LIGHT_BLUE_200,
                        actions=[
                            
                                ft.IconButton(tooltip=data['name'], icon=ft.icons.ACCOUNT_CIRCLE_SHARP, on_click=profile_settings),
                                
                            ],
                        ),
                    navigation_bar = ft.NavigationBar(
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
                    ),
                    controls = [
                                dashboard
                            ],
                )
            )
            page.update()

        def view_pop(e):
            print("View pop:", e.view)
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        page.on_route_change = route_change
        page.on_view_pop = view_pop



        
        page.go(page.route)



    ft.app(target=main, view=ft.WEB_BROWSER, assets_dir="media/", port=5000, host="0.0.0.0")