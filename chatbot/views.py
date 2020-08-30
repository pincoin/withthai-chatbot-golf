import logging
import re

import linebot
from django.http import (
    HttpResponse, HttpResponseForbidden
)
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from linebot import models
from linebot.exceptions import InvalidSignatureError

from chatbot.models import WebhookRequestLog
from golf import models as golf_models
from .handlers import (
    message, follow, unfollow
)


@method_decorator(csrf_exempt, name='dispatch')
class CallbackView(generic.View):
    def __init__(self):
        super(CallbackView, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.line_bot_api = None
        self.handler = None

    def post(self, request, *args, **kwargs):
        golf_club = golf_models.GolfClub.objects.get(slug=self.kwargs['slug'])
        self.line_bot_api = linebot.LineBotApi(golf_club.line_bot_channel_access_token)
        self.handler = linebot.WebhookHandler(golf_club.line_bot_channel_secret)

        @self.handler.add(models.MessageEvent, message=models.TextMessage)
        def handle_message(event):
            text = event.message.text.strip().lower()

            if match := re \
                    .compile('New\s"(.+)"\s(\d\d\d\d-\d\d-\d\d)\s(\d\d:\d\d)\s(\d)PAX\s(\d)CART', re.I) \
                    .match(text):
                message.command_new(event, self.line_bot_api, match=match, golf_club=golf_club)
            elif text == 'booking':
                message.command_booking(event, self.line_bot_api)
            elif text in ['price', 'rate', 'fee']:
                message.command_price(event, self.line_bot_api)
            elif text in ['course', 'club']:
                message.command_course(event, self.line_bot_api, golf_club=golf_club)
            elif text in ['promotions', 'promotion']:
                message.command_promotions(event, self.line_bot_api)
            elif text in ['deals', 'deal', 'hot']:
                message.command_deals(event, self.line_bot_api)
            elif text in ['coupons', 'coupon']:
                message.command_coupons(event, self.line_bot_api)
            elif text in ['settings', 'profile']:
                message.command_settings(event, self.line_bot_api)
            elif text in ['location', 'map']:
                message.command_location(event, self.line_bot_api, golf_club=golf_club)
            elif text in ['caddies', 'caddie']:
                message.command_caddies(event, self.line_bot_api)
            elif text == 'layout':
                message.command_layout(event, self.line_bot_api)
            elif text in ['hotels', 'hotel', 'accommodation', 'accommodations']:
                message.command_hotels(event, self.line_bot_api)
            elif text in ['restaurants', 'restaurant', 'food']:
                message.command_restaurants(event, self.line_bot_api)
            else:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(
                        text='Touch the button to send a message.',
                        quick_reply=models.QuickReply(
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
                            ])))

        @self.handler.add(models.PostbackEvent)
        def handle_post_back(event):
            self.line_bot_api.reply_message(
                event.reply_token,
                models.TextSendMessage(text=f'{event.postback.data} {event.postback.params}'))

        @self.handler.add(models.FollowEvent)
        def handle_follow(event):
            follow.command_follow(event, self.line_bot_api, golf_club=golf_club)

        @self.handler.add(models.UnfollowEvent)
        def handle_unfollow(event):
            unfollow.command_unfollow(event, self.line_bot_api, golf_club=golf_club)

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
