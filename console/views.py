import re

from django.shortcuts import get_object_or_404
from django.template.defaultfilters import date
from django.utils import timezone
from django.views import generic

from conf import tasks
from golf import models as golf_models
from . import forms
from . import viewmixins


class HomeView(generic.TemplateView):
    template_name = 'console/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context


class GolfBookingOrderListView(viewmixins.EnglishContextMixin, generic.ListView):
    template_name = 'console/golf_booking_order_list.html'

    context_object_name = 'orders'

    form_clas = forms.SearchForm

    def get_queryset(self):
        queryset = golf_models.GolfBookingOrder.objects \
            .select_related('customer_group') \
            .filter(golf_club__slug=self.kwargs['slug'])

        if 'search' in self.request.GET and self.request.GET['search'] \
                and 'keyword' in self.request.GET and self.request.GET['keyword']:
            search = self.request.GET['search'].strip()

            if search == 'round_date' \
                    and re.compile('\d{4}-\d{2}-\d{2}').match(keyword := self.request.GET['keyword'].strip()):
                queryset = queryset \
                    .filter(round_date=keyword)
            elif search == 'customer_name' \
                    and len(keyword := self.request.GET['keyword'].strip()) > 2:
                queryset = queryset \
                    .filter(fullname__icontains=keyword)

        if 'order_status' in self.request.GET and self.request.GET['order_status']:
            order_status = self.request.GET['order_status'].strip()

            if order_status == 'open':
                queryset = queryset \
                    .filter(order_status=golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open)
            elif order_status == 'offered':
                queryset = queryset \
                    .filter(order_status=golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.offered)
            elif order_status == 'accepted':
                queryset = queryset \
                    .filter(order_status=golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.accepted)
            elif order_status == 'confirmed':
                queryset = queryset \
                    .filter(order_status=golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.confirmed)
            elif order_status == 'closed':
                queryset = queryset \
                    .filter(order_status=golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.closed)

        if 'payment_status' in self.request.GET and self.request.GET['payment_status']:
            payment_status = self.request.GET['payment_status']

            if payment_status == 'unpaid':
                queryset = queryset \
                    .filter(payment_status=golf_models.GolfBookingOrder.PAYMENT_STATUS_CHOICES.unpaid)
            elif payment_status == 'paid':
                queryset = queryset \
                    .filter(payment_status=golf_models.GolfBookingOrder.PAYMENT_STATUS_CHOICES.paid)
            elif payment_status == 'refund_requests':
                queryset = queryset \
                    .filter(payment_status=golf_models.GolfBookingOrder.PAYMENT_STATUS_CHOICES.refund_requests)
            elif payment_status == 'refunded':
                queryset = queryset \
                    .filter(payment_status=golf_models.GolfBookingOrder.PAYMENT_STATUS_CHOICES.refunded)

        if 'day' in self.request.GET and self.request.GET['day']:
            day = self.request.GET['day']

            if day == 'today':
                queryset = queryset \
                    .filter(round_date=timezone.datetime.today())
            elif day == 'tomorrow':
                queryset = queryset \
                    .filter(round_date=timezone.datetime.today() + timezone.timedelta(days=1))

        if 'sort' in self.request.GET and self.request.GET['sort']:
            sort = self.request.GET['sort']

            if sort == 'round_date':
                return queryset.order_by('-round_date', '-round_time')
            elif sort == 'booking_date':
                return queryset.order_by('-created', )

        return queryset.order_by('-created', )

    def get_context_data(self, **kwargs):
        context = super(GolfBookingOrderListView, self).get_context_data(**kwargs)

        block_size = 5
        start_index = int((context['page_obj'].number - 1) / block_size) * block_size
        end_index = min(start_index + block_size, len(context['paginator'].page_range))

        context['slug'] = self.kwargs['slug']

        context['page_range'] = context['paginator'].page_range[start_index:end_index]

        context['form'] = self.form_clas(
            search=self.request.GET.get('search') if self.request.GET.get('search') else 'round_date',
            keyword=self.request.GET.get('keyword') if self.request.GET.get('keyword') else '',
            order_status=self.request.GET.get('order_status') if self.request.GET.get('order_status') else '',
            payment_status=self.request.GET.get('payment_status') if self.request.GET.get('payment_status') else '',
            sort=self.request.GET.get('sort') if self.request.GET.get('sort') else '',
        )

        return context

    def get_paginate_by(self, queryset):
        # items per page
        return 10


class GolfBookingOrderDetailView(viewmixins.EnglishContextMixin, generic.DetailView):
    template_name = 'console/golf_booking_order_detail.html'

    context_object_name = 'order'

    confirm_form_class = forms.ConfirmForm
    offer_form_class = forms.OfferForm
    reject_form_class = forms.RejectForm

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = golf_models.GolfBookingOrder.objects \
            .select_related('customer_group', 'golf_club') \
            .filter(order_no=self.kwargs['uuid'])

        return get_object_or_404(queryset)

    def get_context_data(self, **kwargs):
        context = super(GolfBookingOrderDetailView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']

        context['confirm_form'] = self.confirm_form_class()
        context['offer_form'] = self.offer_form_class()
        context['reject_form'] = self.reject_form_class()

        context['products'] = golf_models.GolfBookingOrderProduct.objects \
            .select_related('customer_group') \
            .filter(order__order_no=self.kwargs['uuid']) \
            .order_by('product')

        context['logs'] = golf_models.GolfBookingOrderStatusLog.objects \
            .select_related('user') \
            .filter(order__order_no=self.kwargs['uuid']) \
            .order_by('-created')

        return context


class GolfBookingOrderConfirmView(viewmixins.OrderChangeContextMixin, generic.FormView):
    form_class = forms.ConfirmForm

    def __init__(self):
        super(GolfBookingOrderConfirmView, self).__init__()
        self.object = None

    def form_valid(self, form):
        if self.object.order_status in [golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open,
                                        golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.accepted]:
            self.object.round_time = form.cleaned_data['round_time']
            self.object.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.confirmed
            self.object.save()

            round_date_formatted = date(self.object.round_date, 'Y-m-d')
            round_time_formatted = date(self.object.round_time, 'H:i')

            log = golf_models.GolfBookingOrderStatusLog()
            log.order = self.object
            log.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.confirmed
            log.payment_status = self.object.payment_status
            log.message = f'{round_date_formatted} {round_time_formatted}\n{self.object.pax} PAX {self.object.cart} CART\n'
            log.save()

            to = self.object.line_user.line_user_id
            message = 'Booking confirmed.\n\n' \
                      f'Round Date/Time: {round_date_formatted} {round_time_formatted}\n' \
                      f'Golfer #: {self.object.pax}\n' \
                      f'Cart #: {self.object.cart}\n' \
                      f'Total: {self.object.total_selling_price:,.0f} THB\n\n' \
                      'Thank you.'

            tasks.send_push_text_message_line.delay(self.object.golf_club.line_bot_channel_access_token, to, message)

        return super(GolfBookingOrderConfirmView, self).form_valid(form)


class GolfBookingOrderOfferView(viewmixins.OrderChangeContextMixin, generic.FormView):
    form_class = forms.OfferForm

    def __init__(self):
        super(GolfBookingOrderOfferView, self).__init__()
        self.object = None

    def form_valid(self, form):
        if self.object.order_status in [golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open, ]:
            self.object.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.offered
            self.object.save()

            round_date_formatted = date(self.object.round_date, 'Y-m-d')
            round_time_formatted = ', '.join(form.cleaned_data['tee_off_times'])

            log = golf_models.GolfBookingOrderStatusLog()
            log.order = self.object
            log.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.offered
            log.payment_status = self.object.payment_status
            log.message = f'{round_date_formatted} [{round_time_formatted}]\n{self.object.pax} PAX {self.object.cart} CART\n'
            log.save()

            to = self.object.line_user.line_user_id
            message = 'Tee-off time offer.\n\n' \
                      'Please, choose your appropriate tee time. Otherwise, you may close the booking.\n\n' \
                      'Thank you.'

            postback_actions = []

            for tee_time in form.cleaned_data['tee_off_times']:
                postback_actions.append({
                    'label': f'{round_date_formatted} {tee_time}',
                    'data': f'action=accept&golf_club={self.object.golf_club.slug}&order_no={self.object.order_no}&tee_time={tee_time}',
                    'display_text': f'Accept {round_date_formatted} {tee_time}',
                })

            postback_actions.append({
                'label': 'Close',
                'data': f'action=close&golf_club={self.object.golf_club.slug}&order_no={self.object.order_no}',
                'display_text': 'Close',
            })

            tasks.send_push_text_message_line.delay(self.object.golf_club.line_bot_channel_access_token,
                                                    to, message, postback_actions=postback_actions)

        return super(GolfBookingOrderOfferView, self).form_valid(form)


class GolfBookingOrderRejectView(viewmixins.OrderChangeContextMixin, generic.FormView):
    form_class = forms.RejectForm

    def __init__(self):
        super(GolfBookingOrderRejectView, self).__init__()
        self.object = None

    def form_valid(self, form):
        if self.object.order_status in [golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open, ]:
            self.object.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.closed
            self.object.save()

            round_date_formatted = date(self.object.round_date, 'Y-m-d')
            round_time_formatted = date(self.object.round_time, 'H:i')

            log = golf_models.GolfBookingOrderStatusLog()
            log.order = self.object
            log.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.closed
            log.payment_status = self.object.payment_status
            log.message = f'{round_date_formatted} {round_time_formatted}\n{self.object.pax} PAX {self.object.cart} CART\n'
            log.save()

            to = self.object.line_user.line_user_id
            message = 'Booking closed.\n\n' \
                      'We apologize for the inconvenience ' \
                      'because your tee time is not available.\n\n' \
                      'Please, make a new booking with another round date/time.\n\n' \
                      'Thank you.'

            tasks.send_push_text_message_line.delay(self.object.golf_club.line_bot_channel_access_token, to, message)

        return super(GolfBookingOrderRejectView, self).form_valid(form)
