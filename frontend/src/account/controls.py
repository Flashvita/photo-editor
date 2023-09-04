import requests
import json
import time
import threading

from flet import (
    CrossAxisAlignment,
    Container,
    Column,
    ElevatedButton,
    Image,
    ImageFit,
    UserControl,
    KeyboardType,
    TextField,
    Text,
    MainAxisAlignment,
    View,
    border_radius,
    icons,
    colors
)

from app_settings.settings import CORS_ORIGIN

from src.utils import (
    validate_phone_number,
    send_sms,
    error_input_number
)


class TimeOut(UserControl):
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
        Text("Available")

    def build(self):
        self.countdown = Text()
        return self.countdown


class Registration(UserControl):
    """Registration user with input data
    """
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.seconds = 30
        self.phone_number = TextField(
                                        label="Номер телефона",
                                        prefix_text="+7",
                                        keyboard_type=KeyboardType.PHONE,
                                        max_length=10,
                                    )
      
        self.first_name = TextField(
                                        label="Имя",
                                        capitalization=True,
                                    )
        self.last_name = TextField(
                                        label="Фамилия",
                                        capitalization=True,
                                    )
        self.password = TextField(
                            label="Пароль",
                            password=True,
                            can_reveal_password=True,
                        )
        self.retry_password = TextField(
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
        self.password.error_text = 'Пароли не совпадают'
        self.retry_password.error_text = 'Пароли не совпадают'
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
                    View(
                        "/verification/phone_number",
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        vertical_alignment=MainAxisAlignment.CENTER,
                        controls=[Container(
                                            border_radius=border_radius.all(5),
                                            content=Column(
                                                            width=600,
                                                            controls=[
                                                                    TextField(
                                                                            label="Введите код подтверждения",
                                                                            keyboard_type=KeyboardType.NUMBER,
                                                                            max_length=4,
                                                                            ),
                                ElevatedButton(text="Подтвердить", on_click=self.register_account),
                                TimeOut(30),
                        ]
                    )
                )
            ]
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
                #Successful registration
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
            self.page.add(Text(f"User not created, error:{data['message']}!!!"))
            self.page.update()

    def build(self):
        self.login_view = Container(
                    border_radius=border_radius.all(5),
                    content = Column(
                    width = 600,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls = [
                    self.phone_number,
                    self.first_name,
                    self.last_name,
                    self.password,
                    self.retry_password,
                    
                    ElevatedButton(
                                        text="Зарегестрироваться",
                                        color=colors.ORANGE,
                                        icon=icons.SEND_ROUNDED,
                                        on_click=self.go_registration
                                    ),
                    ]
                )
        )
        return self.login_view


class Login(UserControl):
    """Main Page app for choices log-in or sign-in
    """
    def __init__(self, page):
        super().__init__()
        self.page = page
        # self.img = Image(
        # src=f"/icons/photo_label.png",
        # width=100,
        # height=100,
        # fit=ImageFit.CONTAIN,
        #     )
        self.phone_number = TextField(
                        label="Номер телефона",
                        prefix_text="+7",
                        keyboard_type="PHONE",
                        max_length=10,
                        # bgcolor=ft.colors.BROWN_200,
                    )
        self.password = TextField(
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
        self.page.go("/account/registration")
    
    def go_recover(self, e):
        self.page.go("/account/recover-password")

    def build(self):
        self.login_view = Container(
                    border_radius=border_radius.all(15),
                    content = Column(
                    width = 600,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls = [
                    Image(
        src=f"/icons/photo_label.png",
        width=100,
        height=100,
        fit=ImageFit.CONTAIN,
            ),
                    self.phone_number,
                    self.password,
                    ElevatedButton(
                                    text="Войти",
                                    icon=icons.LOGIN,
                                    on_click=self.user_login,
                                    icon_color=colors.BLUE,
                                ),
                    Text(value="Еще нет аккаунта?"),
                    ElevatedButton(
                                    text="Зарегестрироваться",
                                    #icon=ft.icons.FOLLOW_THE_SIGNS,
                                    #icon_color=ft.colors.YELLOW,
                                    on_click=self.get_registration_view
                                ),
                    Text(value="Забыл пароль?"),
                    ElevatedButton(
                                    text="Восстановить",
                                    #icon=ft.icons.TEXTSMS_ROUNDED,
                                    #icon_color=ft.colors.BLUE,
                                    on_click=self.go_recover
                                ),
                    ]
                )
        )

        return self.login_view


class SendSms(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.phone_number = TextField(
                        label="Номер телефона",
                        prefix_text="+7",
                        keyboard_type="PHONE",
                        max_length=10,
                        # bgcolor=ft.colors.BROWN_200,
                    )

    def go_verify_device(self, e):
        print('e', e)
        self.number = f"{self.phone_number.prefix_text}{self.phone_number.value}"
        print('self.number', self.number)
        if not validate_phone_number(self.number):
            return error_input_number(self)
        self.code = send_sms(self.number)
        self.page.views.append(

        )


    def build(self):
        self.sms_view = Container(
                    border_radius=border_radius.all(15),
                    content = Column(
                    width = 600,
                    # horizontal_alignment = CrossAxisAlignment.CENTER,
                    # vertical_alignment = MainAxisAlignment.CENTER,
                    controls = [
                    Text(value="Введите номер телефона указанный при регистрации вам поступит смс"),
                    self.phone_number,
                    ElevatedButton(
                                    text="Получить код восстановления",
                                    on_click=self.go_verify_device
                                    
                    )
                    ]
                )
        )
        return self.sms_view