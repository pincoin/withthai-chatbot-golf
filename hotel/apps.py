from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HotelConfig(AppConfig):
    name = 'hotel'
    verbose_name = _('hotel')
