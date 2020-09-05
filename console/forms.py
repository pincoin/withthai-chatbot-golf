from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ConfirmForm(forms.Form):
    round_time = forms.TimeField(required=True)

    def clean_round_time(self):
        data = self.cleaned_data['round_time']

        if data < timezone.datetime.strptime('06:00', '%H:%M').time() \
                or data > timezone.datetime.strptime('20:00', '%H:%M').time():
            raise forms.ValidationError(_('Invalid round time'))

        return data


class OfferForm(forms.Form):
    tee_off_times = forms.TimeField(widget=forms.HiddenInput(), required=False)

    def clean_tee_off_times(self):
        tee_off_times = list(filter(None, self.data.getlist('tee_off_times')))

        if len(tee_off_times) == 0:
            raise forms.ValidationError(_('No round time is offered.'))

        return tee_off_times


class RejectForm(forms.Form):
    pass
