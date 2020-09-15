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


class OfferForm(forms.Form):
    tee_off_times = forms.TimeField(widget=forms.HiddenInput(), required=False)

    def clean_tee_off_times(self):
        tee_off_times = list(filter(None, self.data.getlist('tee_off_times')))

        if len(tee_off_times) == 0:
            raise forms.ValidationError(_('No round time is offered.'))

        return tee_off_times


class RejectForm(forms.Form):
    pass


class OrderSearchForm(forms.Form):
    search = forms.ChoiceField(
        choices=(
            ('round_date', _('Date'),),
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
            ('unpaid', _('Not paid'),),
            ('paid', _('Paid'),),
            ('refund_requests', _('Refund requests'),),
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

        super(OrderSearchForm, self).__init__(*args, **kwargs)

        self.fields['search'].initial = search
        self.fields['keyword'].initial = keyword
        self.fields['order_status'].initial = order_status
        self.fields['payment_status'].initial = payment_status
        self.fields['sort'].initial = sort


class GolfClubForm(forms.ModelForm):
    class Meta:
        model = golf_models.GolfClub
        fields = ('slug',)


class GreenFeeSearchForm(forms.Form):
    seasons = forms.ModelChoiceField(
        queryset=None,
        empty_label=_('Seasons'),
        required=False,
    )

    day_of_week = forms.ChoiceField(
        choices=[('', _('Day of Week'))] + golf_models.Timeslot.DAY_CHOICES,
        required=False,
    )

    timeslots = forms.ModelChoiceField(
        queryset=None,
        empty_label=_('Timeslots'),
        required=False,
    )

    customer_groups = forms.ModelChoiceField(
        queryset=None,
        empty_label=_('Customer Groups'),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        slug = kwargs.pop('slug', '')
        seasons = kwargs.pop('seasons', '')
        day_of_week = kwargs.pop('day_of_week', '')
        timeslots = kwargs.pop('timeslots', '')
        customer_groups = kwargs.pop('customer_groups', '')

        super(GreenFeeSearchForm, self).__init__(*args, **kwargs)

        if slug:
            self.fields['seasons'].queryset = golf_models.Season.objects \
                .filter(golf_club__slug=slug) \
                .order_by('-season_end')

            self.fields['seasons'].label_from_instance = lambda obj: \
                f'{obj.season_start} {obj.season_end}'

            self.fields['timeslots'].queryset = golf_models.Timeslot.objects \
                .filter(golf_club__slug=slug) \
                .order_by('day_of_week', 'slot_start')

            self.fields['timeslots'].label_from_instance = lambda obj: \
                f'{obj.slot_start:%H:%M} {obj.slot_end:%H:%M} ({obj.title_english})'

            self.fields['customer_groups'].queryset = golf_models.CustomerGroup.objects \
                .filter(golf_club__slug=slug) \
                .order_by('position')

            self.fields['customer_groups'].label_from_instance = lambda obj: \
                f'{obj.title_english}'

        self.fields['seasons'].initial = seasons
        self.fields['day_of_week'].initial = day_of_week
        self.fields['timeslots'].initial = timeslots
        self.fields['customer_groups'].initial = customer_groups
