from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from golf import models as golf_models


class ConfirmForm(forms.Form):
    round_time = forms.TimeField(required=True)

    def clean_round_time(self):
        data = self.cleaned_data['round_time']

        if data < timezone.datetime.strptime('06:00', '%H:%M').time() \
                or data > timezone.datetime.strptime('20:00', '%H:%M').time():
            raise forms.ValidationError(_('Invalid round time'))

        return data


class OfferForm(forms.ModelForm):
    class Meta:
        model = golf_models.GolfBookingOrder
        fields = ()


class RejectForm(forms.Form):
    pass
