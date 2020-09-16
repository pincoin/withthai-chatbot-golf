from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from ipware.ip import get_client_ip

from . import models


@receiver(user_logged_in)
def login_logger(request, user, **kwargs):
    login_log = models.LoginLog()
    login_log.user = user
    login_log.ip_address = get_client_ip(request)
    login_log.save()
