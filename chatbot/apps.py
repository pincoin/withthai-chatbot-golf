from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ChatbotConfig(AppConfig):
    name = 'chatbot'
    verbose_name = _('chatbot')
