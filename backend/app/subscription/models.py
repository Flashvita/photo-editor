from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import timedelta
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from commons.utils.enhanced_models import upload_by_models


class SubscriptionTypes(models.IntegerChoices):
    ONE_MONTH = 1
    TWO_MONT = 2
    THREE_MONT = 3
    SIX_MONTH = 6
    YEAR = 12

class Subscription(models.Model):
    title = models.CharField(max_length=100)
    period = models.PositiveIntegerField(choices=SubscriptionTypes.choices)
    image = models.ImageField(
        upload_to=upload_by_models,
        null=True,
        blank=True
    )
    description = models.TextField(max_length=500)
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.title}"


class UserSubscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_subscriptions",
    )
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="type_subscription"
    )
    currency = models.CharField(max_length=10)
    price = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    finish_date = models.DateTimeField(null=True, blank=True)
    payed = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    auto_renewal = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.pk}"

    # def save(self, **kwargs):
    #     if self.created.month in [1, 3, 5, 7, 8, 10, 12]:
    #         self.finish_date = self.created + timedelta(days=31)
    #     if self.created.month == 2:
    #         if self.created.year % 4 == 0:
    #             self.finish_date = self.created + timedelta(days=29)
    #         else:
    #             self.finish_date = self.created + timedelta(days=28)
    #     if self.created.month in [4, 6, 9, 11]:
    #         self.finish_date = self.created + timedelta(days=30)
    #     return super().save()
    

    # Check subscription to expired 
    @property
    def expired(self):
        return timezone.now() > self.finish_date





