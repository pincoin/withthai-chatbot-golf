from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class MyAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # Prevent Django local sign up
        if request.path.rstrip('/') == reverse('account_signup').rstrip('/'):
            return False
        return True


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def validate_disconnect(self, account, accounts):
        # Prevent disconnection
        raise ValidationError(_('You cannot disconnect social media account.'))
