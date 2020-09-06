import datetime

from django.template.defaultfilters import date
from django.urls import reverse
from django.utils import timezone
from linebot import models

from conf import tasks
from golf import models as golf_models
from .. import utils
from .. import validators


def command_new(event, line_bot_api, **kwargs):
    golf_club = kwargs['golf_club']
    match = kwargs['match']

    # New "John Doe" 2020-08-10 12:30 3 GOLFER 3 CART

    # 1. Retrieve LINE user
    try:
        membership = golf_models.LineUserMembership.objects \
            .select_related('line_user', 'customer_group') \
            .get(line_user__line_user_id=event.source.user_id,
                 customer_group__golf_club=golf_club)
    except golf_models.LineUserMembership.DoesNotExist:
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text='Invalid Golf Course or LINE ID'))
        return

    # 2. Check if N unpaid booking exist
    if (count := golf_models.GolfBookingOrder.objects
            .filter(golf_club=golf_club,
                    line_user=membership.line_user,
                    order_status__in=[golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open,
                                      golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.offered,
                                      golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.accepted,
                                      golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.confirmed],
                    payment_status=golf_models.GolfBookingOrder.PAYMENT_STATUS_CHOICES.unpaid)
            .count()) >= golf_club.multiple_booking_orders:
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(
                text=f'You cannot make a new booking because you already have the unpaid {count} booking orders'))
        return

    # 3. Message data validation
    # 3.1 match[4] PAX
    if not validators.validate_pax(pax := int(match[4]), golf_club=golf_club):
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text=f'Invalid Golfer#: {golf_club.min_pax} to {golf_club.max_pax}'))
        return

    # 3.2. match[5] CART
    if not validators.validate_cart(cart := int(match[5]), pax, golf_club=golf_club):
        error_message = 'Invalid Cart#'

        if golf_club.cart_compulsory == 1:
            error_message = 'Invalid Cart#: Cart required'
        elif golf_club.cart_compulsory > 1:
            if pax >= golf_club.cart_compulsory:
                error_message = f'Invalid Cart#: Cart required {golf_club.cart_compulsory}+ Golfer'
            else:
                error_message = 'Invalid Cart#'

        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text=error_message))
        return

    # 3.3. match[1] Customer name
    if not validators.validate_customer_name(customer_name := match[1]):
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text='Invalid Customer Name: Your name must be written in Thai or English.'))
        return

    # 3.4. match[2] Round date
    if not validators.validate_round_date(round_date := timezone.datetime.strptime(match[2], '%Y-%m-%d'),
                                          holiday := utils.is_holiday(round_date),
                                          golf_club=golf_club):
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text=f'Invalid Round Date'))
        return

    # 3.5. match[3] Round time
    if not validators.validate_round_time(round_time := timezone.datetime.strptime(match[3], '%H:%M').time(),
                                          golf_club=golf_club):
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text=f'Invalid Round Time'))
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
            models.TextSendMessage(text='Invalid Booking Data'))
        return

    # 4. Calculate fees
    # 4.1. Green fee
    green_fee = golf_models.GolfBookingOrderProduct()
    green_fee.product = golf_models.GolfBookingOrderProduct.PRODUCT_CHOICES.green_fee
    green_fee.list_price = fees[0].list_price
    green_fee.selling_price = fees[0].selling_price
    green_fee.quantity = pax
    green_fee.customer_group = membership.customer_group

    # 4.2. Caddie fee
    caddie_fee = golf_models.GolfBookingOrderProduct()
    caddie_fee.product = golf_models.GolfBookingOrderProduct.PRODUCT_CHOICES.caddie_fee
    caddie_fee.list_price = fees[0].season.caddie_fee_list_price
    caddie_fee.selling_price = fees[0].season.caddie_fee_selling_price
    caddie_fee.quantity = pax
    caddie_fee.customer_group = membership.customer_group

    # 4.3. Cart fee
    cart_fee = None

    if cart > 0:
        cart_fee = golf_models.GolfBookingOrderProduct()
        cart_fee.product = golf_models.GolfBookingOrderProduct.PRODUCT_CHOICES.cart_fee
        cart_fee.list_price = fees[0].season.cart_fee_list_price
        cart_fee.selling_price = fees[0].season.cart_fee_selling_price
        cart_fee.quantity = cart
        cart_fee.customer_group = membership.customer_group

    # 5. Save models
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
                             + cart_fee.list_price_subtotal if cart_fee else 0
    order.total_selling_price = green_fee.subtotal + caddie_fee.subtotal \
                                + cart_fee.subtotal if cart_fee else 0
    order.order_status = order.ORDER_STATUS_CHOICES.open
    order.payment_status = order.PAYMENT_STATUS_CHOICES.unpaid
    order.save()

    green_fee.order = order
    caddie_fee.order = order

    if cart_fee:
        cart_fee.order = order

    golf_models.GolfBookingOrderProduct.objects \
        .bulk_create([green_fee, caddie_fee, cart_fee] if cart_fee else [green_fee, caddie_fee])

    # 5.1 Logging
    round_date_formatted = date(round_date, 'Y-m-d')
    round_time_formatted = date(round_time, 'H:i')

    log = golf_models.GolfBookingOrderStatusLog()
    log.order = order
    log.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open
    log.payment_status = golf_models.GolfBookingOrder.PAYMENT_STATUS_CHOICES.unpaid
    log.message = f'{round_date_formatted} {round_time_formatted}\n{pax} PAX {cart} CART\n'
    log.save()

    # 6. Notification to golf club
    url = reverse('console:golf-booking-order-detail', args=(golf_club.slug, order.order_no))

    notification = (
        f'New\n"{customer_name}"\n{round_date_formatted}\n{round_time_formatted}\n{pax} GOLFER\n{cart} CART\n'
        f'https://www.withthai.com{url}'
    )
    tasks.send_notification_line.delay(golf_club.line_notify_access_token, notification)

    # 7. Notification to customer
    now = timezone.localtime().time()

    if golf_club.business_hour_start <= now <= golf_club.business_hour_end:
        message = 'We will notify you of the available tee-off date/time within 15 minutes.'
    elif golf_club.business_hour_end < now <= datetime.time(23, 59, 59):
        message = 'We will notify you of the available tee-off date/time after 8 am tomorrow morning.'
    else:  # datetime.time(0, 0, 0) <= now < golf_club.business_hour_start
        message = 'We will notify you of the available tee-off date/time after 8 am this morning.'

    # 8. Reply message
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text=message))


def command_booking(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='booking list - carousel message',
                               quick_reply=models.QuickReply(
                                   items=[
                                       models.QuickReplyButton(
                                           action=models.MessageAction(label='My Profile',
                                                                       text='Profile')),
                                   ])))


def command_price(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='Price Table - flex or template message'))


def command_course(event, line_bot_api, **kwargs):
    golf_club = kwargs['golf_club']

    line_bot_api.reply_message(
        event.reply_token, [
            models.FlexSendMessage(
                alt_text=golf_club.title_english,
                contents=golf_club.info)])


def command_promotions(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='promotions - carousel message'))


def command_deals(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='deals - carousel message'))


def command_coupons(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='coupons - carousel message'))


def command_settings(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='settings - carousel message'))


def command_location(event, line_bot_api, **kwargs):
    golf_club = kwargs['golf_club']

    line_bot_api.reply_message(
        event.reply_token, [
            models.LocationSendMessage(title=golf_club.title_english,
                                       address=golf_club.address,
                                       latitude=float(golf_club.latitude),
                                       longitude=float(golf_club.longitude))])


def command_caddies(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='caddies - carousel message'))


def command_layout(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.ImageSendMessage(
            original_content_url='https://loremflickr.com/cache/resized/3553_3806423994_1c05ef2e12_z_640_360_nofilter.jpg',
            preview_image_url='https://loremflickr.com/cache/resized/3553_3806423994_1c05ef2e12_z_640_360_nofilter.jpg'))


def command_hotels(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='hotels - carousel message'))


def command_restaurants(event, line_bot_api, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='restaurants - carousel message'))
