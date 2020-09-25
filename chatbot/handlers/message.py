import copy
import datetime
import logging

from django.template.defaultfilters import date
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from linebot import models

from conf import tasks
from golf import models as golf_models
from golf import utils as golf_utils
from .. import decorators
from .. import utils
from .. import validators


@decorators.translation_activate
def command_new(event, line_bot_api, **kwargs):
    logger = logging.getLogger(__name__)

    match = kwargs['match']
    golf_club = kwargs['golf_club']
    membership = kwargs['membership']

    # New "John Doe" 2020-08-10 12:30 3 GOLFER 3 CART

    # 1. Check if N unpaid booking exist
    if (count := golf_models.GolfBookingOrder.objects
            .filter(golf_club=golf_club,
                    line_user=membership.line_user,
                    order_status__in=[golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open,
                                      golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.offered,
                                      golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.accepted,
                                      golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.confirmed],
                    payment_status=golf_models.GolfBookingOrder.PAYMENT_STATUS_CHOICES.unpaid,
                    invisible=False)
            .count()) >= golf_club.multiple_booking_orders:
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(
                text=_('You cannot make a new booking because you already have the unpaid {} booking orders')
                    .format(count)))
        return

    # 2. Message data validation
    # 2.1 match[4] PAX
    if not validators.validate_pax(pax := int(match[4]), golf_club=golf_club):
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text=_('Invalid Golfer#: {} to {}').format(golf_club.min_pax, golf_club.max_pax)))
        return

    # 2.2. match[5] CART
    if not validators.validate_cart(cart := int(match[5]), pax, golf_club=golf_club):
        error_message = _('Invalid Cart#')

        if golf_club.cart_compulsory == 1:
            error_message = _('Invalid Cart#: Cart required')
        elif golf_club.cart_compulsory > 1:
            if pax >= golf_club.cart_compulsory:
                error_message = _('Invalid Cart#: Cart required {}+ Golfer').format(golf_club.cart_compulsory)
            else:
                error_message = _('Invalid Cart#')

        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text=error_message))
        return

    # 2.3. match[1] Customer name
    if not validators.validate_customer_name(customer_name := match[1]):
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text=_('Invalid Customer Name: Your name must be written in Thai or English.')))
        return

    # 2.4. match[2] Round date
    if not validators.validate_round_date(round_date := timezone.datetime.strptime(match[2], '%Y-%m-%d'),
                                          holiday := utils.is_holiday(round_date),
                                          golf_club=golf_club):
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text=_('Invalid Round Date')))
        return

    # 2.5. match[3] Round time
    if not validators.validate_round_time(round_time := timezone.datetime.strptime(match[3], '%H:%M').time(),
                                          golf_club=golf_club):
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text=_('Invalid Round Time')))
        return

    fees = golf_models.GreenFee.objects \
        .filter(season__golf_club=golf_club,
                season__season_start__lte=round_date,
                season__season_end__gte=round_date,
                timeslot__golf_club=golf_club,
                timeslot__slot_start__lte=round_time,
                timeslot__slot_end__gte=round_time,
                timeslot__day_of_week=1 if holiday else 0,
                customer_group__golf_club=golf_club,
                customer_group=membership.customer_group)

    if len(fees) != 1:
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text=_('Invalid Booking Data')))
        return

    # 3. Calculate fees
    # 3.1. Green fee
    green_fee = golf_models.GolfBookingOrderProduct()
    green_fee.product = golf_models.GolfBookingOrderProduct.PRODUCT_CHOICES.green_fee
    green_fee.list_price = fees[0].list_price
    green_fee.selling_price = fees[0].selling_price
    green_fee.quantity = pax
    green_fee.customer_group = membership.customer_group

    # 3.2. Caddie fee
    caddie_fee = golf_models.GolfBookingOrderProduct()
    caddie_fee.product = golf_models.GolfBookingOrderProduct.PRODUCT_CHOICES.caddie_fee
    caddie_fee.list_price = fees[0].season.caddie_fee_list_price
    caddie_fee.selling_price = fees[0].season.caddie_fee_selling_price
    caddie_fee.quantity = pax
    caddie_fee.customer_group = membership.customer_group

    # 3.3. Cart fee
    cart_fee = None

    if cart > 0:
        cart_fee = golf_models.GolfBookingOrderProduct()
        cart_fee.product = golf_models.GolfBookingOrderProduct.PRODUCT_CHOICES.cart_fee
        cart_fee.list_price = fees[0].season.cart_fee_list_price
        cart_fee.selling_price = fees[0].season.cart_fee_selling_price
        cart_fee.quantity = cart
        cart_fee.customer_group = membership.customer_group

    # 4. Save models
    order = golf_models.GolfBookingOrder()
    order.golf_club = golf_club
    order.line_user = membership.line_user
    order.fullname = customer_name
    order.customer_group = membership.customer_group
    order.round_date = round_date
    order.round_time = round_time
    order.pax = pax
    order.cart = cart
    order.total_list_price = green_fee.list_price_subtotal + caddie_fee.list_price_subtotal \
                             + (cart_fee.list_price_subtotal if cart_fee else 0)
    order.total_selling_price = green_fee.subtotal + caddie_fee.subtotal \
                                + (cart_fee.subtotal if cart_fee else 0)
    order.order_status = order.ORDER_STATUS_CHOICES.open
    order.payment_status = order.PAYMENT_STATUS_CHOICES.unpaid
    order.save()

    green_fee.order = order
    caddie_fee.order = order

    if cart_fee:
        cart_fee.order = order

    golf_models.GolfBookingOrderProduct.objects \
        .bulk_create([green_fee, caddie_fee, cart_fee] if cart_fee else [green_fee, caddie_fee])

    # 4.1 Logging
    round_date_formatted = date(round_date, 'Y-m-d')
    round_time_formatted = date(round_time, 'H:i')

    golf_utils.log_order_status(order,
                                golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open,
                                golf_models.GolfBookingOrder.PAYMENT_STATUS_CHOICES.unpaid,
                                f'{round_date_formatted} {round_time_formatted}\n'
                                f'{pax} PAX {cart} CART\n')

    # 5. Notification to golf club
    url = reverse('console:golf-booking-order-detail', args=(golf_club.slug, order.order_no))

    notification = (
        f'New\n"{customer_name}"\n{round_date_formatted}\n{round_time_formatted}\n{pax} GOLFER\n{cart} CART\n'
        f'https://www.withthai.com{url}'
    )
    tasks.send_notification_line.delay(golf_club.line_notify_access_token, notification)

    # 6. Notification to customer
    now = timezone.localtime().time()

    if golf_club.business_hour_start <= now <= golf_club.business_hour_end:
        message = _('We will notify you of the available tee-off date/time within 15 minutes.')
    elif golf_club.business_hour_end < now <= datetime.time(23, 59, 59):
        message = _('We will notify you of the available tee-off date/time after 8 am tomorrow morning.')
    else:  # datetime.time(0, 0, 0) <= now < golf_club.business_hour_start
        message = _('We will notify you of the available tee-off date/time after 8 am this morning.')

    # 7. Reply message
    response = _('''New Booking

Round Date/Time: {0} {1}
Golfer #: {2}
Cart #: {3}
Total: {4:,.0f} THB

Thank you.''').format(round_date_formatted, round_time_formatted, pax, cart, order.total_selling_price)

    line_bot_api.reply_message(
        event.reply_token, [
            models.TextSendMessage(text=response),
            models.TextSendMessage(text=message)])


@decorators.translation_activate
def command_booking(event, line_bot_api, **kwargs):
    golf_club = kwargs['golf_club']

    orders = golf_models.GolfBookingOrder.objects \
                 .select_related('golf_club', 'user', 'line_user', 'customer_group') \
                 .prefetch_related('golfbookingorderproduct_set', 'golfbookingordertimeoffer_set') \
                 .filter(line_user__line_user_id=event.source.user_id,
                         round_date__gte=timezone.make_aware(timezone.localtime().today()),
                         invisible=False) \
                 .exclude(order_status=golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.closed) \
                 .order_by('order_status', 'round_date')[:10]

    order_list = []

    for order in orders:
        order_flex_message = copy.deepcopy(golf_club.order_flex_message)

        round_time_formatted = date(order.round_time, 'H:i')

        order_flex_message['body']['contents'][0]['contents'][0]['text'] = f'{order.round_date} {round_time_formatted}'
        order_flex_message['body']['contents'][0]['contents'][1]['text'] = _('{} PAX {} CART') \
            .format(order.pax, order.cart)
        order_flex_message['body']['contents'][1]['text'] = f'{order.fullname}'
        order_flex_message['body']['contents'][2]['contents'][0]['text'] = order.get_order_status_display()
        order_flex_message['body']['contents'][2]['contents'][1]['text'] = order.get_payment_status_display()
        '''
        order_flex_message['footer']['contents'][0]['action']['uri'] \
            = f"https://liff.line.me/{golf_club.liff['request']['id']}"
        '''

        if order.order_status == order.ORDER_STATUS_CHOICES.open:
            order_flex_message['body']['contents'].append(
                {
                    'type': 'separator',
                    'margin': 'xl',
                }
            )
            order_flex_message['body']['contents'].append(
                {
                    'type': 'text',
                    'text': _('Not Confirmed Yet'),
                    'color': '#b71c1c',
                    'margin': 'md'
                }
            )
            order_flex_message['body']['contents'].append(
                {
                    'type': 'text',
                    'text': _('Please, wait for the confirmation or tee time offers.'),
                    'wrap': True,
                    'margin': 'md'
                }
            )
            order_flex_message['footer'] = {
                'type': 'box',
                'layout': 'vertical',
                'contents': [
                    {
                        'type': 'separator',
                        'margin': 'md'
                    },
                    {
                        'type': 'button',
                        'action': {
                            'type': 'uri',
                            'label': _('New Booking Inquiry'),
                            'uri': f"https://liff.line.me/{golf_club.liff['request']['id']}"
                        },
                        'style': 'primary',
                        'height': 'sm',
                        'color': '#00acc1',
                        'margin': 'md'
                    }
                ]
            }
        elif order.order_status == order.ORDER_STATUS_CHOICES.offered:
            order_flex_message['body']['contents'].append(
                {
                    'type': 'separator',
                    'margin': 'xl',
                }
            )
            order_flex_message['body']['contents'].append(
                {
                    'type': 'text',
                    'text': _('Please, choose tee time as shown below or close your booking.'),
                    'wrap': True,
                    'margin': 'md'
                }
            )

            order_flex_message['footer'] = {
                'type': 'box',
                'layout': 'vertical',
                'contents': [
                    {
                        'type': 'separator',
                        'margin': 'xl'
                    },
                    {
                        'type': 'button',
                        'action': {
                            'type': 'postback',
                            'label': _('Close Booking'),
                            'data': f'action=close&golf_club={order.golf_club.slug}&order_no={order.order_no}',
                            'displayText': _('Close Booking')
                        },
                        'margin': 'md',
                        'height': 'sm',
                        'style': 'primary',
                        'color': '#e53935'
                    },
                    {
                        'type': 'separator',
                        'margin': 'xl'
                    },
                    {
                        'type': 'button',
                        'action': {
                            'type': 'uri',
                            'label': _('New Booking Inquiry'),
                            'uri': f"https://liff.line.me/{golf_club.liff['request']['id']}"
                        },
                        'style': 'primary',
                        'height': 'sm',
                        'color': '#00acc1',
                        'margin': 'md'
                    }
                ]
            }

            tee_times = []

            round_date_formatted = date(order.round_date, 'Y-m-d')

            for tee_time in order.golfbookingordertimeoffer_set.all():
                tee = date(tee_time.round_time, 'H:i')

                tee_times.append(
                    {
                        'type': 'button',
                        'action': {
                            'type': 'postback',
                            'label': f'{tee}',
                            'data': f'action=accept&golf_club={order.golf_club.slug}'
                                    f'&order_no={order.order_no}&tee_time={tee}',
                            'displayText': _('Accept {} {}').format(round_date_formatted, tee),
                        },
                        'margin': 'md',
                        'color': '#039be5',
                        'style': 'primary',
                        'height': 'sm'
                    }
                )

            if tee_times:
                order_flex_message['footer']['contents'] = tee_times + order_flex_message['footer']['contents']

        elif order.order_status == order.ORDER_STATUS_CHOICES.accepted:
            order_flex_message['body']['contents'].append(
                {
                    'type': 'separator',
                    'margin': 'xl',
                }
            )
            order_flex_message['body']['contents'].append(
                {
                    'type': 'text',
                    'text': _('Please, wait for the confirmation.'),
                    'wrap': True,
                    'margin': 'md'
                }
            )
            order_flex_message['footer'] = {
                'type': 'box',
                'layout': 'vertical',
                'contents': [
                    {
                        'type': 'separator',
                        'margin': 'md'
                    },
                    {
                        'type': 'button',
                        'action': {
                            'type': 'uri',
                            'label': _('New Booking Inquiry'),
                            'uri': f"https://liff.line.me/{golf_club.liff['request']['id']}"
                        },
                        'style': 'primary',
                        'height': 'sm',
                        'color': '#00acc1',
                        'margin': 'md'
                    }
                ]
            }
        else:
            order_flex_message['footer'] = {
                'type': 'box',
                'layout': 'vertical',
                'contents': [
                    {
                        'type': 'separator',
                        'margin': 'md'
                    },
                    {
                        'type': 'button',
                        'action': {
                            'type': 'uri',
                            'label': _('New Booking Inquiry'),
                            'uri': f"https://liff.line.me/{golf_club.liff['request']['id']}"
                        },
                        'style': 'primary',
                        'height': 'sm',
                        'color': '#00acc1',
                        'margin': 'md'
                    }
                ]
            }

        order_flex_message['body']['contents'][8]['contents'][1]['text'] = _('{0:,.0f} THB') \
            .format(order.total_selling_price)

        idx = 4
        for fee in order.golfbookingorderproduct_set.all():
            order_flex_message['body']['contents'][idx]['contents'][0]['text'] = fee.get_product_display()
            order_flex_message['body']['contents'][idx]['contents'][1]['text'] = _('{0:,.0f} x {1} = {2:,.0f} THB') \
                .format(fee.selling_price, fee.quantity, fee.subtotal)
            idx += 1

        if order.cart == 0:
            del order_flex_message['body']['contents'][6]

        order_list.append(order_flex_message)

    if orders:
        line_bot_api.reply_message(
            event.reply_token, [
                models.FlexSendMessage(
                    alt_text='My Booking List',
                    contents=models.CarouselContainer(contents=order_list))])

    else:
        no_order_flex_message = copy.deepcopy(golf_club.no_order_flex_message)
        no_order_flex_message['body']['contents'][2]['action']['uri'] \
            = f"https://liff.line.me/{golf_club.liff['request']['id']}"

        line_bot_api.reply_message(
            event.reply_token, [
                models.FlexSendMessage(
                    alt_text='No Booking Yet',
                    contents=no_order_flex_message)
            ])


@decorators.translation_activate
def command_course(event, line_bot_api, **kwargs):
    golf_club = kwargs['golf_club']

    line_bot_api.reply_message(
        event.reply_token, [
            models.FlexSendMessage(
                alt_text=golf_club.title_english,
                contents=golf_club.info_flex_message)])


@decorators.translation_activate
def command_promotions(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='promotions - carousel message'))


@decorators.translation_activate
def command_deals(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='deals - carousel message'))


@decorators.translation_activate
def command_coupons(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='coupons - carousel message'))


@decorators.translation_activate
def command_settings(event, line_bot_api, **kwargs):
    match = kwargs['match']
    membership = kwargs['membership']

    membership.line_user.fullname = match[1]
    membership.line_user.email = match[2]
    membership.line_user.phone = match[3]
    membership.line_user.lang = match[4]
    membership.line_user.save()

    line_bot_api.reply_message(
        event.reply_token, [
            models.TextSendMessage(text=f'Your profile has been saved: {match[1]} {match[2]} {match[3]} {match[4]}')])


@decorators.translation_activate
def command_location(event, line_bot_api, **kwargs):
    golf_club = kwargs['golf_club']

    line_bot_api.reply_message(
        event.reply_token, [
            models.LocationSendMessage(title=golf_club.title_english,
                                       address=golf_club.address,
                                       latitude=float(golf_club.latitude),
                                       longitude=float(golf_club.longitude))])


@decorators.translation_activate
def command_caddies(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='caddies - carousel message'))


@decorators.translation_activate
def command_layout(event, line_bot_api, **kwargs):
    layout = kwargs['layout']

    line_bot_api.reply_message(
        event.reply_token,
        models.ImageSendMessage(
            original_content_url=layout,
            preview_image_url=layout))


@decorators.translation_activate
def command_hotels(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='hotels - carousel message'))


@decorators.translation_activate
def command_restaurants(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='restaurants - carousel message'))
