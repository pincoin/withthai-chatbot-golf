from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import models as model_utils_models


class WebhookRequestLog(model_utils_models.TimeStampedModel):
    request_header = models.TextField(
        verbose_name=_('Request header'),
        blank=True,
    )

    request_body = models.TextField(
        verbose_name=_('Request body'),
        blank=True,
    )

    class Meta:
        verbose_name = _('Webhook request log')
        verbose_name_plural = _('Webhook request logs')


class EventLog(model_utils_models.TimeStampedModel):
    class Meta:
        verbose_name = _('Event log')
        verbose_name_plural = _('Event logs')


class MessageLog(model_utils_models.TimeStampedModel):
    class Meta:
        verbose_name = _('Message log')
        verbose_name_plural = _('Message logs')
