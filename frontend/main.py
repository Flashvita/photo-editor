import flet as ft

import requests
import json

from app_settings.routers import routes

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
    Page,
    Text,
    View,
    colors,
    RouteChangeEvent
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
        
        def view_pop(e):
            print("View pop:", e.view)
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        page.on_route_change = routes # List Router app
        page.on_view_pop = view_pop
        
        page.go(page.route)


    ft.app(target=main, view=ft.WEB_BROWSER, assets_dir="assert/", port=5000, host="0.0.0.0")




