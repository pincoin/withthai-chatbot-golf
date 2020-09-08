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


class SearchForm(forms.Form):
    search = forms.ChoiceField(
        choices=(
            ('round_date', _('Round Date'),),
            ('customer_name', _('Customer'),),
        ),
        required=False,
    )

    keyword = forms.TimeField(
        label=_('Keyword'),
        required=False,
        widget=forms.TimeInput(
            attrs={
                'class': 'input is-fullwidth',
                'placeholder': _('HH:MM'),
            }
        ),
    )

    order_status = forms.ChoiceField(
        choices=(
            ('', _('Order Status'),),
            ('open', _('Open'),),
            ('offered', _('Offered'),),
            ('accepted', _('Accepted'),),
            ('confirmed', _('Confirmed'),),
            ('closed', _('Closed'),),
        ),
        required=False,
    )

    payment_status = forms.ChoiceField(
        choices=(
            ('', _('Payment Status'),),
            ('unpaid', _('Unpaid'),),
            ('paid', _('Paid'),),
            ('refund_requests', _('Refund Requests'),),
            ('refunded', _('Refunded'),),
        ),
        required=False,
    )

    sort = forms.ChoiceField(
        choices=(
            ('booking_date', _('Booking Date'),),
            ('round_date', _('Round Date'),),
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        search = kwargs.pop('search', 'round_date')
        keyword = kwargs.pop('keyword', '')
        order_status = kwargs.pop('order_status', '')
        payment_status = kwargs.pop('payment_status', '')
        sort = kwargs.pop('sort', 'booking_date')

        super(SearchForm, self).__init__(*args, **kwargs)

        self.fields['search'].initial = search
        self.fields['keyword'].initial = keyword
        self.fields['order_status'].initial = order_status
        self.fields['payment_status'].initial = payment_status
        self.fields['sort'].initial = sort
