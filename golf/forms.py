from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class RateAdminForm(forms.ModelForm):
    golf_club = forms.FloatField(
        label=_('Golf club'),
    )

    class Meta:
        model = models.Rate
        exclude = ()
