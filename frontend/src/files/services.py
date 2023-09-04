
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
    
# def routes(obj):
#     from flet import FilePicker, FilePickerResultEvent
#     page = obj.page
#     if page.route == "/":
#         def pick_files_result(e: FilePickerResultEvent):
#             selected_files.value = (
#                 ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
#             )
#             selected_files.update()
#         pick_files_dialog = FilePicker(on_result=pick_files_result)
#         selected_files = Text()