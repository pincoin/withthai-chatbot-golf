from allauth.account import forms as allauthforms
from allauth.socialaccount import forms as allauthsocialforms
from django import forms
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from . import models


class MemberSignupForm(allauthsocialforms.SignupForm):
    first_name = forms.CharField(
        label=_('First name'),
        max_length=30,
        help_text=_('First name written in English'),
        widget=forms.TextInput(),
        validators=[RegexValidator('^[A-Z]+$', message=_('Uppercase alphabet only')), ],
    )

    last_name = forms.CharField(
        label=_('Last name'),
        max_length=30,
        help_text=_('Last name written in English'),
        widget=forms.TextInput(),
        validators=[RegexValidator('^[A-Z]+$', message=_('Uppercase alphabet only')), ],
    )

    phone = forms.CharField(
        label=_('Telephone'),
        max_length=20,
        widget=forms.TextInput(),
        help_text=_('Digits or plus sign only'),
        validators=[RegexValidator('^\+?1?\d{9,20}$', message=_('Invalid phone number format')), ],
    )

    def __init__(self, *args, **kwargs):
        super(MemberSignupForm, self).__init__(*args, **kwargs)

    def custom_signup(self, request, user):
        # Required fields for Django default model
        user.first_name = self.cleaned_data['first_name'].strip()
        user.last_name = self.cleaned_data['last_name'].strip()

        # Default group: customers
        g = Group.objects.get(name='Customers')
        user.groups.add(g)
        user.save()

        # Required fields for profile model
        profile = models.Profile()
        profile.user = user

        profile.save()


class MemberChangePasswordForm(allauthforms.ChangePasswordForm):
    def clean(self):
        raise forms.ValidationError(_('You cannot change password.'))


class MemberSetPasswordForm(allauthforms.SetPasswordForm):
    def clean(self):
        raise forms.ValidationError(_('You cannot set password.'))


class MemberResetPasswordForm(allauthforms.ResetPasswordForm):
    def clean(self):
        raise forms.ValidationError(_('You cannot reset password.'))


class MemberAddEmailForm(allauthforms.AddEmailForm):
    def clean(self):
        raise forms.ValidationError(_('You cannot add an email.'))
