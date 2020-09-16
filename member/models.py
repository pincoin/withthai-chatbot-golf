from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class Profile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        verbose_name=_('Telephone'),
        max_length=16,
        blank=True,
        null=True,
    )

    total_order_count = models.IntegerField(
        verbose_name=_('Total order count'),
        default=0,
    )

    first_purchased = models.DateTimeField(
        verbose_name=_('First purchased date'),
        null=True,
    )

    last_purchased = models.DateTimeField(
        verbose_name=_('Last purchased date'),
        null=True,
    )

    max_price = models.DecimalField(
        verbose_name=_('Max price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    total_selling_price = models.DecimalField(
        verbose_name=_('Total selling price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    average_price = models.DecimalField(
        verbose_name=_('Average price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    mileage = models.DecimalField(
        verbose_name=_('Mileage'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    memo = models.TextField(
        verbose_name=_('User memo'),
        blank=True,
    )

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return f'{self.id} profile - user {self.user.id}/{self.user.username}'


class LoginLog(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP address'),
    )

    class Meta:
        verbose_name = _('Login log')
        verbose_name_plural = _('Login logs')

    def __str__(self):
        return f'{self.user.email} {self.ip_address} {self.created}'
