import re

from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import date
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.generic.edit import FormMixin

from conf import tasks
from golf import models as golf_models
from golf import utils as golf_utils
from . import forms
from . import viewmixins


class HomeView(generic.TemplateView):
    template_name = 'console/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context


class GolfBookingOrderListView(viewmixins.PageableMixin, generic.ListView):
    template_name = 'console/golf_booking_order_list.html'

    context_object_name = 'orders'

    form_class = forms.OrderSearchForm

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

        context['slug'] = self.kwargs['slug']

        querystring = self.request.GET.copy()
        context['q'] = querystring.urlencode()

        if 'page' in querystring:
            querystring.pop('page')
            context['q_popped'] = querystring.urlencode()
        else:
            context['q_popped'] = context['q']

        keyword = None

        if 'day' in self.request.GET and self.request.GET['day']:
            day = self.request.GET['day']

            if day == 'today':
                keyword = date(timezone.datetime.today(), 'Y-m-d')
            elif day == 'tomorrow':
                keyword = date(timezone.datetime.today() + timezone.timedelta(days=1), 'Y-m-d')
        else:
            keyword = self.request.GET.get('keyword') if self.request.GET.get('keyword') else ''

        context['form'] = self.form_class(
            search=self.request.GET.get('search') if self.request.GET.get('search') else 'round_date',
            keyword=keyword,
            order_status=self.request.GET.get('order_status') if self.request.GET.get('order_status') else '',
            payment_status=self.request.GET.get('payment_status') if self.request.GET.get('payment_status') else '',
            sort=self.request.GET.get('sort') if self.request.GET.get('sort') else '',
        )

        return context


class GolfBookingOrderDetailView(FormMixin, generic.DetailView):
    template_name = 'console/golf_booking_order_detail.html'

    context_object_name = 'order'

    form_class = forms.ConfirmForm
    offer_form_class = forms.OfferForm
    reject_form_class = forms.RejectForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form_class = None
        form_name = ''

        if 'form' in request.POST:
            if request.POST['form'] == 'confirm-form':
                form_class = self.get_form_class()
                form_name = 'confirm_form'
            elif request.POST['form'] == 'offer-form':
                form_class = self.offer_form_class
                form_name = 'offer_form'
            elif request.POST['form'] == 'reject-form':
                form_class = self.reject_form_class
                form_name = 'reject_form'

        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(**{form_name: form})
        else:
            return self.form_invalid(**{form_name: form})

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = golf_models.GolfBookingOrder.objects \
            .select_related('customer_group', 'golf_club') \
            .filter(order_no=self.kwargs['uuid'])

        return get_object_or_404(queryset)

    def form_valid(self, **kwargs):
        form_name = None

        if 'confirm_form' in kwargs:
            form_name = 'confirm_form'

            if self.object.order_status in [golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open,
                                            golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.accepted]:
                self.object.round_time = kwargs[form_name].cleaned_data['round_time']
                self.object.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.confirmed
                self.object.save()

                round_date_formatted = date(self.object.round_date, 'Y-m-d')
                round_time_formatted = date(self.object.round_time, 'H:i')

                golf_utils.log_order_status(self.object,
                                            golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.confirmed,
                                            self.object.payment_status,
                                            f'{round_date_formatted} {round_time_formatted}\n'
                                            f'{self.object.pax} PAX {self.object.cart} CART\n')

                to = self.object.line_user.line_user_id
                message = 'Booking confirmed.\n\n' \
                          f'Round Date/Time: {round_date_formatted} {round_time_formatted}\n' \
                          f'Golfer #: {self.object.pax}\n' \
                          f'Cart #: {self.object.cart}\n' \
                          f'Total: {self.object.total_selling_price:,.0f} THB\n\n' \
                          'Thank you.'

                tasks.send_push_text_message_line.delay(self.object.golf_club.line_bot_channel_access_token, to,
                                                        message)
        elif 'offer_form' in kwargs:
            form_name = 'offer_form'

            if self.object.order_status in [golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open, ]:
                self.object.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.offered
                self.object.save()

                round_date_formatted = date(self.object.round_date, 'Y-m-d')
                round_time_formatted = ', '.join(kwargs[form_name].cleaned_data['tee_off_times'])

                golf_utils.log_order_status(self.object,
                                            golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.offered,
                                            self.object.payment_status,
                                            f'{round_date_formatted} [{round_time_formatted}]\n'
                                            f'{self.object.pax} PAX {self.object.cart} CART\n')

                to = self.object.line_user.line_user_id
                message = 'Tee-off time offer.\n\n' \
                          'Please, choose your appropriate tee time. Otherwise, you may close the booking.\n\n' \
                          'Thank you.'

                postback_actions = []

                for tee_time in kwargs[form_name].cleaned_data['tee_off_times']:
                    postback_actions.append({
                        'label': f'{round_date_formatted} {tee_time}',
                        'data': f'action=accept&golf_club={self.object.golf_club.slug}'
                                f'&order_no={self.object.order_no}&tee_time={tee_time}',
                        'display_text': f'Accept {round_date_formatted} {tee_time}',
                    })

                postback_actions.append({
                    'label': 'Close',
                    'data': f'action=close&golf_club={self.object.golf_club.slug}&order_no={self.object.order_no}',
                    'display_text': 'Close',
                })

                tasks.send_push_text_message_line.delay(self.object.golf_club.line_bot_channel_access_token,
                                                        to, message, postback_actions=postback_actions)
        elif 'reject_form' in kwargs:
            form_name = 'reject_form'

            if self.object.order_status in [golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open,
                                            golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.accepted]:
                self.object.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.closed
                self.object.save()

                round_date_formatted = date(self.object.round_date, 'Y-m-d')
                round_time_formatted = date(self.object.round_time, 'H:i')

                golf_utils.log_order_status(self.object,
                                            golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.closed,
                                            self.object.payment_status,
                                            f'{round_date_formatted} {round_time_formatted}\n'
                                            f'{self.object.pax} PAX {self.object.cart} CART\n')

                to = self.object.line_user.line_user_id
                message = 'Booking closed.\n\n' \
                          'We apologize for the inconvenience ' \
                          'because your tee time is not available.\n\n' \
                          'Please, make a new booking with another round date/time.\n\n' \
                          'Thank you.'

                tasks.send_push_text_message_line.delay(self.object.golf_club.line_bot_channel_access_token, to,
                                                        message)

        return super(GolfBookingOrderDetailView, self).form_valid(kwargs[form_name])

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(GolfBookingOrderDetailView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']

        if 'confirm_form' not in context:
            context['confirm_form'] = self.form_class(initial={'round_time': self.object.round_time})

        if 'offer_form' not in context:
            context['offer_form'] = self.offer_form_class()

        if 'reject_form' not in context:
            context['reject_form'] = self.reject_form_class()

        context['products'] = golf_models.GolfBookingOrderProduct.objects \
            .select_related('customer_group') \
            .filter(order__order_no=self.kwargs['uuid']) \
            .order_by('product')

        context['logs'] = golf_models.GolfBookingOrderStatusLog.objects \
            .select_related('user') \
            .filter(order__order_no=self.kwargs['uuid']) \
            .order_by('-created')

        context['q'] = self.request.GET.urlencode()

        return context

    def get_success_url(self):
        return reverse('console:golf-booking-order-detail', args=(self.kwargs['slug'], self.object.order_no))


class LineUserListView(viewmixins.PageableMixin, generic.ListView):
    template_name = 'console/line_user_list.html'

    context_object_name = 'users'

    def get_queryset(self):
        queryset = golf_models.LineUserMembership.objects \
            .select_related('line_user', 'customer_group', 'customer_group__golf_club') \
            .filter(customer_group__golf_club__slug=self.kwargs['slug'])

        return queryset.order_by('-line_user__created', )

    def get_context_data(self, **kwargs):
        context = super(LineUserListView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context

    def get_paginate_by(self, queryset):
        # items per page
        return 10


class LineUserDetailView(generic.DetailView):
    template_name = 'console/line_user_detail.html'

    context_object_name = 'user'

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = golf_models.LineUserMembership.objects \
            .select_related('line_user', 'customer_group', 'customer_group__golf_club') \
            .filter(line_user__line_user_id=self.kwargs['line_user_id'])

        return get_object_or_404(queryset)

    def get_context_data(self, **kwargs):
        context = super(LineUserDetailView, self).get_context_data(**kwargs)

        context['slug'] = self.kwargs['slug']
        context['q'] = self.request.GET.urlencode()

        return context


class FacebookUserListView(viewmixins.PageableMixin, generic.ListView):
    pass


class FacebookUserDetailView(generic.DetailView):
    pass


class GolfClubUpdateView(generic.UpdateView):
    template_name = 'console/golf_club_update.html'

    context_object_name = 'golf_club'

    form_class = forms.GolfClubForm

    def get_queryset(self):
        return golf_models.GolfClub.objects \
            .select_related('district', 'customer_group') \
            .filter(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(GolfClubUpdateView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context


class GreenFeeListView(viewmixins.PageableMixin, generic.ListView):
    template_name = 'console/green_fee_list.html'

    context_object_name = 'green_fees'

    form_class = forms.GreenFeeSearchForm

    def get_queryset(self):
        queryset = golf_models.GreenFee.objects \
            .select_related('season', 'timeslot', 'customer_group') \
            .filter(season__golf_club__slug=self.kwargs['slug'],
                    timeslot__golf_club__slug=self.kwargs['slug'],
                    customer_group__golf_club__slug=self.kwargs['slug'])

        if 'seasons' in self.request.GET and self.request.GET['seasons'] \
                and self.request.GET['seasons'].isdigit():
            queryset = queryset \
                .filter(season__id=self.request.GET['seasons'])

        if 'day_of_week' in self.request.GET and self.request.GET['day_of_week'] \
                and self.request.GET['day_of_week'].isdigit():
            queryset = queryset \
                .filter(timeslot__day_of_week=self.request.GET['day_of_week'])

        if 'timeslots' in self.request.GET and self.request.GET['timeslots'] \
                and self.request.GET['timeslots'].isdigit():
            queryset = queryset \
                .filter(timeslot__id=self.request.GET['timeslots'])

        if 'customer_groups' in self.request.GET and self.request.GET['customer_groups'] \
                and self.request.GET['customer_groups'].isdigit():
            queryset = queryset \
                .filter(customer_group__id=self.request.GET['customer_groups'])

        return queryset.order_by('season__season_start',
                                 'timeslot__day_of_week',
                                 'timeslot__slot_start',
                                 'customer_group__position')

    def get_context_data(self, **kwargs):
        context = super(GreenFeeListView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']

        context['form'] = self.form_class(
            slug=self.kwargs['slug'],
            seasons=self.request.GET.get('seasons') if self.request.GET.get('seasons') else '',
            day_of_week=self.request.GET.get('day_of_week') if self.request.GET.get('day_of_week') else '',
            timeslots=self.request.GET.get('timeslots') if self.request.GET.get('timeslots') else '',
            customer_groups=self.request.GET.get('customer_groups') if self.request.GET.get('customer_groups') else '',
        )

        querystring = self.request.GET.copy()
        context['q'] = querystring.urlencode()

        if 'page' in querystring:
            querystring.pop('page')
            context['q_popped'] = querystring.urlencode()
        else:
            context['q_popped'] = context['q']

        return context


class HolidayListView(viewmixins.PageableMixin, generic.ListView):
    template_name = 'console/holiday_list.html'

    context_object_name = 'holidays'

    def get_queryset(self):
        return golf_models.Holiday.objects \
            .order_by('-holiday')

    def get_context_data(self, **kwargs):
        context = super(HolidayListView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context


class SeasonListView(viewmixins.PageableMixin, generic.ListView):
    template_name = 'console/season_list.html'

    context_object_name = 'seasons'

    def get_queryset(self):
        return golf_models.Season.objects \
            .filter(golf_club__slug=self.kwargs['slug']) \
            .order_by('-season_end')

    def get_context_data(self, **kwargs):
        context = super(SeasonListView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context


class TimeslotListView(auth_mixins.LoginRequiredMixin, viewmixins.PageableMixin, generic.ListView):
    template_name = 'console/timeslot_list.html'

    context_object_name = 'timeslots'

    def get_queryset(self):
        return golf_models.Timeslot.objects \
            .filter(golf_club__slug=self.kwargs['slug']) \
            .order_by('day_of_week', 'slot_start')

    def get_context_data(self, **kwargs):
        context = super(TimeslotListView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context
