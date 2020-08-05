from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GolfConfig(AppConfig):
    name = 'golf'
    verbose_name = _('golf')
