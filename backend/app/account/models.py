from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from commons.utils.enhanced_models import upload_by_models


class User(AbstractUser):
    # https://django-phonenumber-field.readthedocs.io/en/latest/reference.html#model-field
    phone_number = PhoneNumberField(
        verbose_name=_("Phone number"),
        unique=True,
        null=True,
    )
    avatar = models.ImageField(
        verbose_name=_("Photo"),
        upload_to=upload_by_models,
        null=True,
        blank=True,
    )

    notification_about_subscribers = models.BooleanField(
        default=True,
        verbose_name=_("Notification about new subscriber")
    )

    def save(self, *args, **kwargs) -> None:
        if self.username != self.phone_number and not self.is_superuser:
            self.username = self.phone_number
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def photo_link(self):
        return f"{settings.MEDIA_URL}{self.avatar}" if self.avatar else None

    def __str__(self) -> str:
        return self.name if len(self.name) > 2 else f"{self.username}"

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
        