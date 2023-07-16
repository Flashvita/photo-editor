
import flet as ft
from utils import (
    send_sms,
    validate_phone_number,
    error_input_number,
)


class SendSms(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.phone_number = ft.TextField(
                        label="Номер телефона",
                        prefix_text="+7",
                        keyboard_type="PHONE",
                        max_length=10,
                        # bgcolor=ft.colors.BROWN_200,
                    )

    def go_verify_device(self):
        self.number = f"{self.phone_number.prefix_text}{self.phone_number.value}"
        if not validate_phone_number(self.number):
            return error_input_number(self)
        self.code = send_sms(self.number)
        self.page.views.append(

        )


    def build(self):
        self.sms_view = ft.Container(
                    border_radius=ft.border_radius.all(15),
                    content = ft.Column(
                    width = 600,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    vertical_alignment = ft.MainAxisAlignment.CENTER,
                    controls = [
                    ft.Text(value="Введите номер телефона указанный при регистрации вам поступит смс"),
                    self.phone_number,
                    ft.ElevatedButton(
                                    text="Получить код восстановления",
                                    on_click=self.go_verify_device
                                    
                    )
                    ]
                )
        )
        return self.sms_view
