from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from account.models import User



@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("username", "first_name", "last_name", "phone_number",  )}),
        (_("Permissions"), {"fields": ("is_active", "is_superuser",
                                       )}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("first_name", "last_name", "phone_number", "password1", "password2"),
        }),
    )
    list_display = ("phone_number", "name", "is_active", "id") #"account_user_key", "is_superuser",
    #list_filter = ("is_active", "account_user_key" )

    ordering = ["-id"]
    
    
