from django import forms

from golf import models as golf_models


class ConfirmForm(forms.ModelForm):
    class Meta:
        model = golf_models.GolfBookingOrder
        fields = (
            'round_time',
        )


class OfferForm(forms.ModelForm):
    class Meta:
        model = golf_models.GolfBookingOrder
        fields = ()


class RejectForm(forms.Form):
    pass
