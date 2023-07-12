

from account.api import account_router
from app.api.api_init import api



api.add_router("/account/", account_router, tags=["Account"])
