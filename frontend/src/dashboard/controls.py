import requests
import json

from app_settings.settings import CORS_ORIGIN


from flet import (
    AppBar,
    UserControl,
    Text,
    Icon,
    PopupMenuButton,
    IconButton,
    PopupMenuItem,
    NavigationBarLabelBehavior,
    NavigationDestination,
    NavigationBar,
    Text,
    View,
    icons,
    colors,
)


class Dashboard(View):
    def __init__(self, page, data):
        super().__init__()
        self.page = page
        self.token = self.page.client_storage.get("access_token")
        self.appbar=AppBar(
                        leading=Icon(icons.PALETTE),
                        leading_width=40,
                        title=Text("Photographer"),
                        center_title=True,
                        bgcolor=colors.LIGHT_BLUE_200,
                        actions=[
                            
                                IconButton(tooltip=data['name'], icon=icons.ACCOUNT_CIRCLE_SHARP, on_click=self.animate_opacityprofile),
                                
                            ],
                        )
        self.navigation_bar = NavigationBar(
                        elevation=30,
                        bgcolor=colors.LIGHT_BLUE_200,
                        label_behavior=NavigationBarLabelBehavior.ALWAYS_HIDE, # Dont work hide label behavior for navigate
                        selected_index=5,
                        destinations=[
                            NavigationDestination(icon=icons.HOME, label="Главная"),
                            NavigationDestination(icon=icons.SEARCH_SHARP, label="Поиск"),
                            NavigationDestination(icon=icons.ADD_A_PHOTO_OUTLINED, label="Добавить фото",),
                            NavigationDestination(
                                icon=icons.CIRCLE_NOTIFICATIONS,
                                label="Уведомления",
                            ),
                            NavigationDestination(
                                icon=icons.FAVORITE,
                                label="Избранное",
                            ), 
                            
                        ],
                        
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

        
class DashboardAppBar(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        self.appbar = AppBar(
        leading=Icon(icons.PALETTE),
        leading_width=40,
        title=Text("AppBar Example"),
        center_title=False,
        bgcolor=colors.SURFACE_VARIANT,
        actions=[
                IconButton(icons.WB_SUNNY_OUTLINED),
                IconButton(icons.FILTER_3),
                PopupMenuButton(
                    items=[
                        PopupMenuItem(text="Item 1"),
                        PopupMenuItem(),  # divider
                        PopupMenuItem(
                            text="Checked item", checked=False
                        ),
                    ]
                ),
            ],
        )
        return  self.appbar
 
  