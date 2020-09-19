from django.template.defaultfilters import date
from django.utils import timezone
from linebot import models

from golf import models as golf_models
from golf import utils as golf_utils
from .. import decorators


@decorators.translation_activate
def command_accept(event, line_bot_api, **kwargs):
    qs = kwargs['qs']

    tee_time = timezone.datetime.strptime(qs['tee_time'], '%H:%M').time()

    order = golf_models.GolfBookingOrder.objects.get(order_no=qs['order_no'])
    order.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.accepted
    order.round_time = tee_time
    order.save()

    round_date_formatted = date(order.round_date, 'Y-m-d')
    round_time_formatted = date(tee_time, 'H:i')

    golf_utils.log_order_status(order,
                                golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.accepted,
                                order.payment_status,
                                f'{round_date_formatted} [{round_time_formatted}]\n'
                                f'{order.pax} PAX {order.cart} CART\n')

    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text=f'You accepted our offer: {round_date_formatted} {round_time_formatted}\n\n'
                                    'We will send you the confirmation notification in a few minutes.\n\n'
                                    'Thank you.'))


@decorators.translation_activate
def command_close(event, line_bot_api, **kwargs):
    qs = kwargs['qs']

    order = golf_models.GolfBookingOrder.objects.get(order_no=qs['order_no'])
    order.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.closed
    order.save()

    round_date_formatted = date(order.round_date, 'Y-m-d')
    round_time_formatted = date(order.round_time, 'H:i')

    golf_utils.log_order_status(order,
                                golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.closed,
                                order.payment_status,
                                f'{round_date_formatted} [{round_time_formatted}]\n'
                                f'{order.pax} PAX {order.cart} CART\n')

    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='You closed your booking.\n\n'
                                    'Please, make a new booking with another round date/time.\n\n'
                                    'Thank you.'))
