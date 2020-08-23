from django.utils.translation import ugettext_lazy as _
from django.views import generic

from golf import models as golf_models
from . import forms
from . import viewmixins


class SampleView(viewmixins.LiffContextMixin, generic.TemplateView):
    app_name = 'sample'

    template_name = 'liff/sample.html'

    def get_context_data(self, **kwargs):
        context = super(SampleView, self).get_context_data(**kwargs)
        context['title'] = _('Sample')
        return context


class GolfBookingCreateFormView(viewmixins.LiffContextMixin, generic.FormView):
    app_name = 'request'

    template_name = 'liff/golf_booking_create_form.html'

    form_class = forms.GolfBookingForm

    def get_context_data(self, **kwargs):
        context = super(GolfBookingCreateFormView, self).get_context_data(**kwargs)
        context['title'] = _('New Booking')
        context['golf_club'] = self.club
        return context


class GolfPriceTableTemplateView(viewmixins.LiffContextMixin, generic.TemplateView):
    app_name = 'price'

    template_name = 'liff/golf_price_table.html'

    def get_context_data(self, **kwargs):
        context = super(GolfPriceTableTemplateView, self).get_context_data(**kwargs)

        green_fees = golf_models.GreenFee.objects \
            .select_related('season', 'timeslot', 'customer_group') \
            .filter(season__golf_club=self.club,
                    timeslot__golf_club=self.club,
                    customer_group__golf_club=self.club) \
            .order_by('season__season_start',
                      'timeslot__day_of_week',
                      'timeslot__slot_start',
                      'customer_group__position')

        seasons = golf_models.Season.objects \
            .filter(golf_club=self.club) \
            .order_by('season_start')

        timeslots = golf_models.Timeslot.objects \
            .filter(golf_club=self.club) \
            .order_by('day_of_week', 'slot_start')

        customer_groups = golf_models.CustomerGroup.objects \
            .filter(golf_club=self.club) \
            .order_by('position')

        price_table = {}
        for green_fee in green_fees:
            if green_fee.season_id not in price_table:
                price_table[green_fee.season_id] = {}

            if green_fee.timeslot_id not in price_table[green_fee.season_id]:
                price_table[green_fee.season_id][green_fee.timeslot_id] = {}

            price_table[green_fee.season_id][green_fee.timeslot_id][green_fee.customer_group_id] = green_fee.list_price

        context['title'] = _('Price Table')

        context['seasons'] = seasons
        context['timeslots'] = timeslots
        context['customer_groups'] = customer_groups

        context['price_table'] = price_table

        return context


class GolfScorecardTemplateView(viewmixins.LiffContextMixin, generic.TemplateView):
    app_name = 'scorecard'

    template_name = 'liff/golf_scorecard.html'

    def get_context_data(self, **kwargs):
        context = super(GolfScorecardTemplateView, self).get_context_data(**kwargs)

        context['title'] = _('Scorecard')
        context['hole'] = range(1, self.club.scorecard['hole'] + 1)
        context['scorecard'] = self.club.scorecard

        return context
