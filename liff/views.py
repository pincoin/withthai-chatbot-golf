from django.utils.translation import ugettext_lazy as _
from django.views import generic

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


class ScorecardTemplateView(viewmixins.LiffContextMixin, generic.TemplateView):
    app_name = 'scorecard'

    template_name = 'liff/scorecard.html'

    def get_context_data(self, **kwargs):
        context = super(ScorecardTemplateView, self).get_context_data(**kwargs)

        context['title'] = _('Scorecard')
        context['hole'] = range(1, self.club.scorecard['hole'] + 1)
        context['scorecard'] = self.club.scorecard

        return context
