from django.utils.translation import ugettext_lazy as _
from django.views import generic

from golf import models as golf_models
from . import forms


class SampleView(generic.TemplateView):
    template_name = 'liff/sample.html'

    def get_context_data(self, **kwargs):
        context = super(SampleView, self).get_context_data(**kwargs)

        context['title'] = _('Sample')

        liff = golf_models.Liff.objects.get(golf_club__slug=self.kwargs['slug'], app_name='sample')

        context['liffId'] = liff.liff_id

        return context


class BookingCreateFormView(generic.FormView):
    template_name = 'liff/booking_create_form.html'

    form_class = forms.BookingForm

    def get_context_data(self, **kwargs):
        context = super(BookingCreateFormView, self).get_context_data(**kwargs)

        context['title'] = _('New Booking')

        liff = golf_models.Liff.objects.get(golf_club__slug=self.kwargs['slug'], app_name='sample')

        context['liffId'] = liff.liff_id

        return context
