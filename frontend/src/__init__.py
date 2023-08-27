from src.account.routes import routes as account_routes
from src.dashboard.routes import routes as dashboard_routes
# from src.profile.routes import routes as profile_routes



def routes(obj):
    page = obj.page
    print("Route change:", obj.route)
    #user_auth(page)
    print("Route after user_auth:", obj.route)
    if page.route.startswith("/account"):
        print("startswith account")
        account_routes(obj)
    if page.route.startswith("/dashboard"):
        dashboard_routes(obj)
    page.update()


