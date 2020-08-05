from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import models as model_utils_models


class WebhookLog(model_utils_models.TimeStampedModel):
    request_header = models.TextField(
        verbose_name=_('Request header'),
        blank=True,
    )

    request_body = models.TextField(
        verbose_name=_('Request body'),
        blank=True,
    )

    response_header = models.TextField(
        verbose_name=_('Response header'),
        blank=True,
    )

    response_body = models.TextField(
        verbose_name=_('Response body'),
        blank=True,
    )

    class Meta:
        verbose_name = _('Webhook log')
        verbose_name_plural = _('Webhook logs')
