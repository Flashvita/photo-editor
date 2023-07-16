import flet as ft

from app_settings.settings import CORS_ORIGIN
import requests
import json 
from utils.phone_number import (
    validate_phone_number,
    error_input_number,
)


class Login(ft.UserControl):
    """Main Page app for choices log-in or sign-in
    """
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.img = ft.Image(
        src=f"assert/icons/photo_label.png",
        width=100,
        height=100,
        fit=ft.ImageFit.CONTAIN,
            )
        self.phone_number = ft.TextField(
                        label="Номер телефона",
                        prefix_text="+7",
                        keyboard_type="PHONE",
                        max_length=10,
                        # bgcolor=ft.colors.BROWN_200,
                    )
        self.password = ft.TextField(
                    label="Пароль",
                    password=True,
                    can_reveal_password=True,
        )

    def get_credential(self, e):
        url = f"{CORS_ORIGIN}api/v1/token/pair"
        data = {
            "password": self.password.value,
            "username": self.number
        }
        response = requests.post(url, data=json.dumps(data))
        return response

    def user_login(self, e):
        self.number = f"{self.phone_number.prefix_text}{self.phone_number.value}"
        if not validate_phone_number(self.number):
            return error_input_number(self)
        response = self.get_credential(e)
        if response.status_code == 200:
            tokens = json.loads(response.content)
            self.page.client_storage.set("refresh_token", tokens["refresh"])
            self.page.client_storage.set("access_token", tokens["access"])
            self.page.go("/dashboard")
        else:
            self.password.error_text = "Неправильный логин или пароль"
            
    
    def get_registration_view(self, e):
        self.page.go("/registration")
    
    def go_recover(self, e):
        self.page.go("/recover-password")

    def build(self):
        self.login_view = ft.Container(
                    border_radius=ft.border_radius.all(15),
                    content = ft.Column(
                    width = 600,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls = [
                    self.img,
                    self.phone_number,
                    self.password,
                    ft.ElevatedButton(
                                    text="Войти",
                                    icon=ft.icons.LOGIN,
                                    on_click=self.user_login,
                                    icon_color=ft.colors.BLUE,
                                ),
                    ft.Text(value="Еще нет аккаунта?"),
                    ft.ElevatedButton(
                                    text="Зарегестрироваться",
                                    #icon=ft.icons.FOLLOW_THE_SIGNS,
                                    #icon_color=ft.colors.YELLOW,
                                    on_click=self.get_registration_view
                                ),
                    ft.Text(value="Забыл пароль?"),
                    ft.ElevatedButton(
                                    text="Восстановить",
                                    #icon=ft.icons.TEXTSMS_ROUNDED,
                                    #icon_color=ft.colors.BLUE,
                                    on_click=self.go_recover
                                ),
                    ]
                )
        )
        return self.login_view