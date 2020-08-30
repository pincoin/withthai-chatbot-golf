import datetime
import logging
import re

import linebot
from django.http import (
    HttpResponse, HttpResponseForbidden
)
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from linebot import models
from linebot.exceptions import InvalidSignatureError

from chatbot.models import WebhookRequestLog
from conf import tasks
from golf import models as golf_models


@method_decorator(csrf_exempt, name='dispatch')
class CallbackView(generic.View):
    def __init__(self):
        super(CallbackView, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.line_bot_api = None
        self.handler = None

        self.help_quick_replies = models.QuickReply(
            items=[
                models.QuickReplyButton(action=models.MessageAction(label='My Booking',
                                                                    text='Booking')),
                models.QuickReplyButton(action=models.MessageAction(label='Price Table',
                                                                    text='Price')),
                models.QuickReplyButton(action=models.MessageAction(label='Course',
                                                                    text='Course')),
                models.QuickReplyButton(action=models.MessageAction(label='Promotions',
                                                                    text='Promotions')),
                models.QuickReplyButton(action=models.MessageAction(label='Coupons',
                                                                    text='Coupons')),
                models.QuickReplyButton(action=models.MessageAction(label='Hot Deals',
                                                                    text='Deals')),
            ])

    def post(self, request, *args, **kwargs):
        golf_club = golf_models.GolfClub.objects.get(slug=self.kwargs['slug'])
        self.logger.info(golf_club.title_english)

        self.line_bot_api = linebot.LineBotApi(golf_club.line_bot_channel_access_token)
        self.handler = linebot.WebhookHandler(golf_club.line_bot_channel_secret)

        @self.handler.add(models.MessageEvent, message=models.TextMessage)
        def handle_message(event):
            text = event.message.text.strip().lower()

            if match := re \
                    .compile('New\s"(.+)"\s(\d\d\d\d-\d\d-\d\d)\s(\d\d:\d\d)\s(\d)PAX\s(\d)CART', re.I) \
                    .match(text):
                # New "John Doe" 2020-08-10 12:30 3PAX 3CART
                # 1. Check if 2 unpaid booking exist

                # 2. Retrieve LINE user
                line_user = golf_models.LineUser.objects.get(line_user_id=event.source.user_id)

                # 3. Booking model
                order = golf_models.GolfBookingOrder()
                order.golf_club = golf_club
                order.line_user = line_user
                order.fullname = match[1]
                order.total_list_price = 0
                order.total_selling_price = 0
                order.save()

                # 4. Fee models

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

                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text=message))
            elif text == 'booking':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='booking list - carousel message',
                                           quick_reply=models.QuickReply(
                                               items=[
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='New Booking',
                                                                                   text='New')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='My Profile',
                                                                                   text='Profile')),
                                               ])))
            elif text in ['price', 'rate', 'fee']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='Price Table - flex or template message',
                                           quick_reply=models.QuickReply(
                                               items=[
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='New Booking',
                                                                                   text='New')),
                                               ])))
            elif text in ['course', 'club']:
                self.line_bot_api.reply_message(
                    event.reply_token, [
                        models.FlexSendMessage(
                            alt_text=golf_club.title_english,
                            contents=golf_club.info)])
            elif text in ['promotions', 'promotion']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='promotions - carousel message',
                                           quick_reply=models.QuickReply(
                                               items=[
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='New Booking',
                                                                                   text='New')),
                                               ])))
            elif text in ['deals', 'deal', 'hot']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='deals - carousel message',
                                           quick_reply=models.QuickReply(
                                               items=[
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='New Booking',
                                                                                   text='New')),
                                               ])))
            elif text in ['coupons', 'coupon']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='coupons - carousel message',
                                           quick_reply=models.QuickReply(
                                               items=[
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='New Booking',
                                                                                   text='New')),
                                               ])))
            elif text in ['settings', 'profile']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='settings - carousel message'))

            elif text in ['location', 'map']:
                self.line_bot_api.reply_message(
                    event.reply_token, [
                        models.LocationSendMessage(title=golf_club.title_english,
                                                   address=golf_club.address,
                                                   latitude=float(golf_club.latitude),
                                                   longitude=float(golf_club.longitude))])
            elif text in ['caddies', 'caddie']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='caddies - carousel message'))
            elif text == 'layout':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.ImageSendMessage(
                        original_content_url='https://loremflickr.com/cache/resized/3553_3806423994_1c05ef2e12_z_640_360_nofilter.jpg',
                        preview_image_url='https://loremflickr.com/cache/resized/3553_3806423994_1c05ef2e12_z_640_360_nofilter.jpg'))
            elif text in ['hotels', 'hotel', 'accommodation', 'accommodations']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='hotels - carousel message'))
            elif text in ['restaurants', 'restaurant', 'food']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='restaurants - carousel message'))

            else:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(
                        text='Touch the button to send a message.',
                        quick_reply=self.help_quick_replies))

        @self.handler.add(models.PostbackEvent)
        def handle_post_back(event):
            self.line_bot_api.reply_message(
                event.reply_token,
                models.TextSendMessage(text=f'{event.postback.data} {event.postback.params}'))

        @self.handler.add(models.FollowEvent)
        def handle_follow(event):
            try:
                user = golf_models.LineUser.objects.get(line_user_id=event.source.user_id)
            except golf_models.LineUser.DoesNotExist:
                user = golf_models.LineUser()
                user.line_user_id = event.source.user_id

            if isinstance(event.source, models.SourceUser):
                profile = self.line_bot_api.get_profile(event.source.user_id)
                user.line_display_name = profile.display_name

            user.follow_status = golf_models.LineUser.FOLLOW_CHOICES.follow
            user.fullname = ''
            user.save()

            membership = golf_models.LineUserMembership()
            membership.line_user = user
            membership.customer_group = golf_club.customer_group
            membership.save()

            self.line_bot_api.reply_message(
                event.reply_token,
                models.TextSendMessage(
                    text='Touch the button to send a message.',
                    quick_reply=self.help_quick_replies))

        @self.handler.add(models.UnfollowEvent)
        def handle_unfollow(event):
            try:
                user = golf_models.LineUser.objects.get(line_user_id=event.source.user_id)
                user.follow_status = golf_models.LineUser.FOLLOW_CHOICES.unfollow
                user.fullname = ''
                user.save()

                membership = golf_models.LineUserMembership \
                    .objects.get(line_user__line_user_id=event.source.user_id,
                                 customer_group__golf_club=golf_club)
                membership.delete()
            except (golf_models.LineUser.DoesNotExist, golf_models.LineUserMembership.DoesNotExist):
                pass

        @self.handler.add(models.JoinEvent)
        def handle_join(event):
            # event.source.user_id mark as joined
            self.line_bot_api.reply_message(
                event.reply_token,
                models.TextSendMessage(text=f'Joined this {event.source.type}')
            )

        @self.handler.add(models.LeaveEvent)
        def handle_leave():
            # event.source.user_id mark as left
            pass

        @self.handler.add(models.MemberJoinedEvent)
        def handle_member_joined(event):
            self.line_bot_api.reply_message(
                event.reply_token,
                models.TextSendMessage(text=f'Got memberJoined event. event={event}')
            )

        @self.handler.add(models.MemberLeftEvent)
        def handle_member_left(event):
            # event.source.user_id mark as left
            pass

        if 'X-Line-Signature' in request.headers:
            signature = request.headers['X-Line-Signature']
            body = request.body.decode('utf-8')

            log = WebhookRequestLog()
            log.request_header = request.headers
            log.request_body = body
            log.save()

            try:
                self.handler.handle(body, signature)
            except InvalidSignatureError:
                return HttpResponseForbidden()

            return HttpResponse('OK')

        return HttpResponseForbidden()
