from django.contrib.admin.views.decorators import staff_member_required
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI(
    title="Photo Editor API",
    version="1.0.0",
    docs_decorator=staff_member_required,
)
api.register_controllers(NinjaJWTDefaultController)
