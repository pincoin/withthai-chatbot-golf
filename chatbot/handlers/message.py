import datetime

from django.utils import timezone
from linebot import models

from conf import tasks
from golf import models as golf_models
from .. import validators


def command_new(event, line_bot_api, **kwargs):
    golf_club = kwargs['golf_club']
    match = kwargs['match']

    # New "John Doe" 2020-08-10 12:30 3PAX 3CART
    # 1. Check if 2 unpaid booking exist

    # 2. Retrieve LINE user
    try:
        membership = golf_models.LineUserMembership.objects \
            .select_related('line_user', 'customer_group') \
            .get(line_user__line_user_id=event.source.user_id,
                 customer_group__golf_club=golf_club)
    except golf_models.LineUserMembership.DoesNotExist:
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text='Invalid golf course or LINE ID'))
        return

    # 2. Check if N unpaid booking exist
    if count := golf_models.GolfBookingOrder.objects \
                        .filter(golf_club=golf_club,
                                line_user=membership.line_user,
                                order_status__in=[golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open,
                                                  golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.offered,
                                                  golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.accepted,
                                                  golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.confirmed],
                                payment_status=golf_models.GolfBookingOrder.PAYMENT_STATUS_CHOICES.unpaid) \
                        .count() >= golf_club.multiple_booking_order:
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(
                text=f'You cannot make a new booking because you already have unpaid {count} booking orders'))

    # 3. Message data validation
    # 3.1 match[4] PAX
    if not validators.validate_pax(pax := int(match[4]), golf_club=golf_club):
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text=f'Invalid PAX: {golf_club.min_pax} to {golf_club.max_pax}'))
        return

    # 3.2. match[5] CART
    if not validators.validate_cart(cart := int(match[5]), pax, golf_club=golf_club):
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text=f'Invalid Cart'))
        return

    # 3.3. match[1] Customer name

    # 3.4. match[2] Round date
    if not validators.validate_round_date(round_date := timezone.datetime.strptime(match[2], '%Y-%m-%d'),
                                          golf_club=golf_club):
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text=f'Invalid round date'))
        return

    # 3.5. match[3] Round time
    round_time = timezone.datetime.strptime(match[3], '%H:%M').time()

    # Season & timeslot & weekday/holiday & customer group & club

    '''
    # 4. Calculate fees
    # 4.1. Green fee
    order_product_list = []

    green_fee = golf_models.GolfBookingOrderProduct()
    green_fee.product = golf_models.GolfBookingOrderProduct.PRODUCT_CHOICES.green_fee
    green_fee.list_price = 0
    green_fee.selling_price = 0
    green_fee.quantity = int(match[4])

    # 4.2. Caddie fee
    caddie_fee = golf_models.GolfBookingOrderProduct()
    caddie_fee.product = golf_models.GolfBookingOrderProduct.PRODUCT_CHOICES.caddie_fee
    caddie_fee.list_price = 0
    caddie_fee.selling_price = 0
    caddie_fee.quantity = int(match[4])

    # 4.3. Cart fee
    if int(match[5]) > 0:
        cart_fee = golf_models.GolfBookingOrderProduct()
        cart_fee.product = golf_models.GolfBookingOrderProduct.PRODUCT_CHOICES.cart_fee
        cart_fee.list_price = 0
        cart_fee.selling_price = 0
        cart_fee.quantity = int(match[5])
    '''

    # 5. Save models
    order = golf_models.GolfBookingOrder()
    order.golf_club = golf_club
    order.line_user = membership.line_user
    order.fullname = match[1]
    order.round_date = round_date
    order.round_time = round_time
    order.pax = pax
    order.cart = cart
    order.total_list_price = 0
    order.total_selling_price = 0
    order.order_status = order.ORDER_STATUS_CHOICES.open
    order.payment_status = order.PAYMENT_STATUS_CHOICES.unpaid
    order.save()

    '''
    green_fee.order = order
    caddie_fee.order = order
    '''

    # 5. Notification to golf club
    notification = f'{match[1]} {match[2]} {match[3]} {match[4]} {match[5]}'
    tasks.send_notification_line.delay(golf_club.line_notify_access_token, notification)

    # 6. Notification to customer
    now = timezone.localtime().time()

    if golf_club.business_hour_start <= now <= golf_club.business_hour_end:
        message = 'We will notify you of the available tee-off date/time within 15 minutes.'
    elif golf_club.business_hour_end < now <= datetime.time(23, 59, 59):
        message = 'We will notify you of the available tee-off date/time after 8 am tomorrow morning.'
    else:  # datetime.time(0, 0, 0) <= now < golf_club.business_hour_start
        message = 'We will notify you of the available tee-off date/time after 8 am this morning.'

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
