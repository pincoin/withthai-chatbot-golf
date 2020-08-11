from django.utils.translation import ugettext_lazy as _
from django.views import generic

from . import forms


class SampleView(generic.TemplateView):
    template_name = 'liff/index2.html'


class BookingCreateFormView(generic.FormView):
    template_name = 'liff/booking_create_form.html'

    form_class = forms.BookingForm

    def get_context_data(self, **kwargs):
        context = super(BookingCreateFormView, self).get_context_data(**kwargs)

        context['title'] = _('New Booking')

        return context
