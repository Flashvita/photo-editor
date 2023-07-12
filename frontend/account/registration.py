import flet as ft
from app_settings.settings import CORS_ORIGIN

import requests
import json



class Registration(ft.UserControl):
    """Registration user with input data
    """
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.username = ft.TextField(
                                        label="Номер телефона",
                                        prefix_text="+7",
                                        keyboard_type=ft.KeyboardType.PHONE,
                                        max_length=10,
                                    )
        self.first_name = ft.TextField(
                                        label="Имя",
                                        capitalization=True,
                                    )
        self.last_name = ft.TextField(
                                        label="Фамилия",
                                        capitalization=True,
                                    )
        self.password = ft.TextField(
                            label="Пароль",
                            password=True,
                            can_reveal_password=True,
                        )
    
         
    def send_registration_data(self, e):
        """
        Make request to api for save user data in database
        """
        url = f'{CORS_ORIGIN}api/v1/account/register'
                
        data = {
                        "username": f"+7{self.username.value}",
                        "first_name": self.first_name.value,
                        "last_name": self.last_name.value,
                        "password": self.password.value,
                        "code": self.code,
                }
        print('data',data)
        response = requests.post(url, data=json.dumps(data))
        return response
    

    def send_sms(self, e):
        """Sending sms to user device for completed registration
        """
        url = f'{CORS_ORIGIN}api/v1/account/send-sms'
                
        data = {
            "phone_number": f"+7{self.username.value}"
        }
        response = requests.post(url, data=json.dumps(data))
        
        data = json.loads(response.content)
        print('response data', data)
        return data
        
        
    def go_registration(self, e):
        self.code = self.send_sms(e)
        self.page.clean()
        self.page.views.append(
                ft.View(
                "/verification/phone_number",
                controls = [ft.TextField(
                                        label="Введите код подтверждения",
                                        keyboard_type=ft.KeyboardType.NUMBER,
                                        max_length=4,
                                    ),
                    ft.ElevatedButton(text="Подтвердить", on_click=self.register_account)]
            )
        )
        self.page.update()

           


    def register_account(self, e):

        response = self.send_registration_data(e)
        if response.status_code == 200:
                # Successful registration
                print('Successful registration', response.content)
                self.user_tokens = json.loads(response.content)
                tokens = json.loads(response.content)
                self.page.client_storage.set("refresh_token", tokens["refresh"])
                self.page.client_storage.set("access_token", tokens["access"])
                storage = self.page.client_storage
                print('storage access_token', storage.get("access_token")) # Токен
                self.page.go("/dashboard")
        else:
            print('Not register registration')
            data = json.loads(response.content)
            self.page.add(ft.Text(f"User not created, error:{data['message']}!!!"))
            self.page.update()

    def build(self):
        self.login_view = ft.Container(
                    border_radius=ft.border_radius.all(5),
                    content = ft.Column(
                    width = 600,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls = [
                    
                    self.username,
                    self.first_name,
                    self.last_name,
                    self.password,
                    ft.TextField(
                            label="Повторите пароль",
                            password=True,
                            can_reveal_password=True,
                        ),
                    
                    ft.ElevatedButton(
                                        text="Зарегестрироваться",
                                        color=ft.colors.ORANGE,
                                        icon=ft.icons.SEND_ROUNDED,
                                        on_click=self.go_registration
                                    ),
                    ]
                )
        )
        return self.login_view