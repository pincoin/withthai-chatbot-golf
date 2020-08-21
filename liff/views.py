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


class BookingCreateFormView(viewmixins.LiffContextMixin, generic.FormView):
    app_name = 'request'

    template_name = 'liff/booking_create_form.html'

    form_class = forms.BookingForm

    def get_context_data(self, **kwargs):
        context = super(BookingCreateFormView, self).get_context_data(**kwargs)
        context['title'] = _('New Booking')
        return context


class PriceTableTemplateView(viewmixins.LiffContextMixin, generic.TemplateView):
    app_name = 'price'

    template_name = 'liff/price.html'

    def get_context_data(self, **kwargs):
        context = super(PriceTableTemplateView, self).get_context_data(**kwargs)

        rates = golf_models.Rate.objects \
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
        for rate in rates:
            if rate.season_id not in price_table:
                price_table[rate.season_id] = {}

            if rate.timeslot_id not in price_table[rate.season_id]:
                price_table[rate.season_id][rate.timeslot_id] = {}

            price_table[rate.season_id][rate.timeslot_id][rate.customer_group_id] = rate.green_fee_list_price

        context['title'] = _('Price Table')

        context['seasons'] = seasons
        context['timeslots'] = timeslots
        context['customer_groups'] = customer_groups

        context['price_table'] = price_table

        return context


class ScorecardTemplateView(viewmixins.LiffContextMixin, generic.TemplateView):
    app_name = 'scorecard'

    template_name = 'liff/scorecard.html'

    def get_context_data(self, **kwargs):
        context = super(ScorecardTemplateView, self).get_context_data(**kwargs)

        context['title'] = _('Scorecard')
        context['hole'] = range(1, self.club.scorecard['hole'] + 1)
        context['scorecard'] = self.club.scorecard

        return context
