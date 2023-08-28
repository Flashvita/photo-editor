from flet import CrossAxisAlignment, MainAxisAlignment, View

from .controls import Login


def user_check_auth(page):
    """
    Check exists token in storage
    for view start page or dashboard
    """
    token = page.client_storage.get("access_token")
    print('token', token)
    if token and page.route == "/account":
        print('go dashboard')
        page.go("/dashboard")
    else:
        login =  Login(page)
        page.views.append(
            View(
                "/account/login",
                horizontal_alignment = CrossAxisAlignment.CENTER,
                vertical_alignment = MainAxisAlignment.CENTER,
                controls = [login],
                )
        )
