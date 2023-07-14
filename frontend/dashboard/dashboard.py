import requests
import json

from app_settings.settings import CORS_ORIGIN

import flet as ft

from flet import (
    UserControl,
    NavigationRailDestination,
    icons,
    colors,
    alignment,
    Row,
    Column,
    Row,
    NavigationRail,
    Text,
    Container,
    border_radius,
    View
)


class Dashboard(View):
    def __init__(self, page, data):
        super().__init__()
        self.page = page
        self.token = self.page.client_storage.get("access_token")
        self.appbar=ft.AppBar(
                        leading=ft.Icon(ft.icons.PALETTE),
                        leading_width=40,
                        title=ft.Text("Photographer"),
                        center_title=True,
                        bgcolor=ft.colors.LIGHT_BLUE_200,
                        actions=[
                            
                                ft.IconButton(tooltip=data['name'], icon=ft.icons.ACCOUNT_CIRCLE_SHARP, on_click=self.animate_opacityprofile),
                                
                            ],
                        )
        self.navigation_bar = ft.NavigationBar(
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
    def profile(self, e):
        self.page.go("/dashboard/profile")
    def build(self):
        headers = {
                        "Authorization": f"Bearer {self.token}"
                    }
        url = f"{CORS_ORIGIN}api/v1/account/users-me"
        response = requests.get(url, headers=headers)
        self.data = json.loads(response.content)
        self.page.client_storage.set("user_data", self.data)
        
        
        return self.appbar

        






















import flet as ft
from flet import (
    UserControl,
    NavigationRailDestination,
    icons,
    colors,
    alignment,
    Row,
    Column,
    Row,
    NavigationRail,
    Text,
    Container,
    border_radius
)


class DashboardAppBar(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        self.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        leading_width=40,
        title=ft.Text("AppBar Example"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
                ft.IconButton(ft.icons.FILTER_3),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Item 1"),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(
                            text="Checked item", checked=False
                        ),
                    ]
                ),
            ],
        )
        return  self.appbar

        
# class Dashboard(UserControl):
 
#     def __init__(self, page):
#         super().__init__()
#         self.page = page
#         self.top_nav_items = [
#             NavigationRailDestination(
#                 label_content=Text("Boards"),
#                 label="Boards",
#                 icon=icons.BOOK_OUTLINED,
#                 selected_icon=icons.BOOK_OUTLINED
#             ),
#             NavigationRailDestination(
#                 label_content=Text("Members"),
#                 label="Members",
#                 icon=icons.PERSON,
#                 selected_icon=icons.PERSON
#             ),
 
#         ]
#         self.top_nav_rail = NavigationRail(
#             selected_index=None,
#             label_type="all",
#             on_change=self.top_nav_change,
#             destinations=self.top_nav_items,
#             bgcolor=colors.BLUE_GREY,
#             extended=True,
#             expand=True
#         )
 
#     def build(self):
#         self.view = Column([
#                 Row([
#                     Text("Workspace"),
#                 ]),
#                 # divider
#                 Container(
#                     bgcolor=colors.BLACK26,
#                     border_radius=border_radius.all(30),
#                     height=1,
#                     alignment=alignment.center_right,
#                     width=220
#                 ),
#                 self.top_nav_rail,
#                 # divider
#                 Container(
#                     bgcolor=colors.BLACK26,
#                     border_radius=border_radius.all(30),
#                     height=1,
#                     alignment=alignment.center_right,
#                     width=220
#                 ),
#             ], tight=True)
            
#         return self.view
 
#     def top_nav_change(self, e):
#         self.top_nav_rail.selected_index = e.control.selected_index
#         self.update()