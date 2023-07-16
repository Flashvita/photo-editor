import flet as ft
from app_settings.settings import CORS_ORIGIN

import requests
import json
import time
import threading
from utils import (
    validate_phone_number,
    send_sms,
    error_input_number
)

class TimeOut(ft.UserControl):
    def __init__(self, seconds):
        super().__init__()
        self.seconds = seconds

    def did_mount(self):
        self.running = True
        self.th = threading.Thread(target=self.update_timer, args=(), daemon=True)
        self.th.start()

    def will_unmount(self):
        self.running = False

    def update_timer(self):
        while self.seconds and self.running:
            mins, secs = divmod(self.seconds, 60)
            self.countdown.value = f"Повторная отправка смс через {mins:02d}:{secs:02d}"
            self.update()
            time.sleep(1)
            self.seconds -= 1
        ft.Text("Available")

    def build(self):
        self.countdown = ft.Text()
        return self.countdown
    


class Registration(ft.UserControl):
    """Registration user with input data
    """
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.seconds = 30
        self.phone_number = ft.TextField(
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
        self.retry_password = ft.TextField(
                            label="Повторите пароль",
                            password=True,
                            can_reveal_password=True,
                        )
    
    
           
    def send_registration_data(self, e):
        """
        Make request to api for save user data in database
        """
        print('send_registration_data')
        url = f'{CORS_ORIGIN}api/v1/account/register'
        data = {
                        "phone_number": self.number,
                        "first_name": self.first_name.value,
                        "last_name": self.last_name.value,
                        "password": self.password.value,
                        "code": self.code,
                }
        print('data', data)
        response = requests.post(url, data=json.dumps(data))
        return response
    

    def password_not_repeated(self, e):
        self.password.error_text='Пароли не совпадают'
        self.retry_password.error_text='Пароли не совпадают'
        self.password.update()
        self.retry_password.update()


    def go_registration(self, e):
        if not self.check_input_password():
            return self.password_not_repeated(self)
        self.number = f"{self.phone_number.prefix_text}{self.phone_number.value}"
        if not validate_phone_number(self.number):
            return error_input_number(self)
        else:            
            # Sending sms after success check input data
            self.code = send_sms(self.number)
            print('self code', self.code)
            self.page.clean()
            self.page.views.append(
                    ft.View(
                    "/verification/phone_number",
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    vertical_alignment = ft.MainAxisAlignment.CENTER,
                    controls = [ft.Container(
                    border_radius=ft.border_radius.all(5),
                    content = ft.Column(
                    width = 600,
                    controls = [ft.TextField(
                                            label="Введите код подтверждения",
                                            keyboard_type=ft.KeyboardType.NUMBER,
                                            max_length=4,
                                        ),
                        ft.ElevatedButton(text="Подтвердить", on_click=self.register_account),
                        TimeOut(30)
                        ]
                    ))]
                    # controls = [ft.TextField(
                    #                         label="Введите код подтверждения",
                    #                         keyboard_type=ft.KeyboardType.NUMBER,
                    #                         max_length=4,
                    #                     ),
                    #     ft.ElevatedButton(text="Подтвердить", on_click=self.register_account),
                    #     TimeOut(30)
                    #     ]
                )
            )
            self.page.update()

           
    def check_input_password(self):
        check = self.password.value == self.retry_password.value
        print('check password', check)
        return check
            

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
                    
                    self.phone_number,
                    self.first_name,
                    self.last_name,
                    self.password,
                    self.retry_password,
                    
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