import flet as ft

from flet import (
    FilePicker,
    FilePickerResultEvent,
    Text,
    Row,
)


def navbar(page):
    navbar = ft.NavigationBar(
                        elevation=30,
                        bgcolor=ft.colors.LIGHT_BLUE_200,
                        label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_HIDE, # Dont work hide label behavior for navigate
                        selected_index=5,
                        destinations=[
                            ft.NavigationDestination(icon=ft.icons.HOME, label="Главная"),
                            ft.NavigationDestination(icon=ft.icons.SEARCH_SHARP, label="Поиск"),
                            ft.NavigationDestination(
                                icon_content=[],
                                icon=ft.icons.ADD_A_PHOTO_OUTLINED,
                                label="Добавить фото"
                                                     
                                                     ),
                            ft.NavigationDestination(
                                icon=ft.icons.CIRCLE_NOTIFICATIONS,
                                label="Уведомления",
                            ),
                            ft.NavigationDestination(
                                icon=ft.icons.FAVORITE,
                                label="Избранное",
                            ), 
                            
                        ],
                        on_change=lambda e: action_navbar_dashboard(page, e.control.selected_index),
                    )
    return navbar
   

def action_navbar_dashboard(page, number_action: int):
    print('number_action=', number_action)
    if number_action == 0:
        print('Главная')
    elif number_action == 1:
        print('Поиск')
    elif number_action == 2:
        print('Добавить фото')
        file_picker = ft.FilePicker()
        file_picker.pick_files(allow_multiple=True)
    elif number_action == 3:
        print('Уведомления')
    elif number_action == 4:
        print('Избранное')


def appbar(data, func):
    appbar = ft.AppBar(
                        leading=ft.Icon(ft.icons.PALETTE),
                        leading_width=40,
                        title=ft.Text("Photoeditor"),
                        center_title=True,
                        bgcolor=ft.colors.LIGHT_BLUE_200,
                        actions=[
                                    ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE_SHARP, on_click=func),
                                ],
                        )
    return appbar


def appbar_profile(data, func):
    appbar = ft.AppBar(
                        elevation=5,
                        leading=ft.Icon(ft.icons.PALETTE),
                        leading_width=40,
                        #title=ft.Text(f"{data['name']}"),
                        title=ft.Text(f"Анна Кулешова"),

                        center_title=True,
                        bgcolor=ft.colors.LIGHT_BLUE_200,
                        actions=[
                            
                                ft.IconButton(icon=ft.icons.SETTINGS, on_click=func),
                                
                            ],
                        )
    return appbar