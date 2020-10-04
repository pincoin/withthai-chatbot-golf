import logging
import re
from urllib.parse import parse_qsl

import linebot
from django import http
from django.conf import settings
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from linebot import models
from linebot.exceptions import InvalidSignatureError

from chatbot.models import WebhookRequestLog
from golf import models as golf_models
from .handlers import (
    message, follow, unfollow, post_back
)


@method_decorator(csrf_exempt, name='dispatch')
class CallbackView(generic.View):
    def __init__(self):
        super(CallbackView, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.line_bot_api = None
        self.handler = None

    def post(self, request, *args, **kwargs):
        cache_key = f"chatbot.views.Callbackview.post({self.kwargs['slug']})"
        cache_time = settings.CACHES['default']['TIMEOUT']

        golf_club = cache.get(cache_key)

        if not golf_club:
            try:
                golf_club = golf_models.GolfClub.objects.get(slug=self.kwargs['slug'])
                cache.set(cache_key, golf_club, cache_time)
            except golf_models.GolfClub.DoesNotExist:
                raise http.Http404('Invalid golf club')

        self.line_bot_api = linebot.LineBotApi(golf_club.line_bot_channel_access_token)
        self.handler = linebot.WebhookHandler(golf_club.line_bot_channel_secret)

        @self.handler.add(models.MessageEvent, message=models.TextMessage)
        def handle_message(event):
            text = event.message.text.strip()
            text_lowercase = text.lower()

            cache_key = f'chatbot.membership({event.source.user_id},{golf_club.id})'
            cache_time = settings.CACHES['default']['TIMEOUT86400']

            membership = cache.get(cache_key)

            # Retrieve LINE user
            if not membership:
                try:
                    membership = golf_models.LineUserMembership.objects \
                        .select_related('line_user', 'customer_group') \
                        .get(line_user__line_user_id=event.source.user_id,
                             customer_group__golf_club=golf_club)
                    cache.set(cache_key, membership, cache_time)
                except golf_models.LineUserMembership.DoesNotExist:
                    self.line_bot_api.reply_message(
                        event.reply_token,
                        models.TextSendMessage(text='Invalid Golf Course or LINE ID'))
                    return

            if match := re \
                    .compile('New\s"(.+)"\s(\d\d\d\d-\d\d-\d\d)\s(\d\d:\d\d)\s(\d)\sGOLFER\s(\d)\sCART', re.I) \
                    .match(text):
                message.command_new(event, self.line_bot_api, match=match,
                                    golf_club=golf_club, membership=membership)
            elif match := re.compile('Settings\s"(.{2,32})"\s([\w.-]+@[\w.-]+)\s([ \d+-]{8,18})\s([a-zA-Z]{2})', re.I) \
                    .match(text):
                message.command_settings(event, self.line_bot_api, match=match,
                                         golf_club=golf_club, membership=membership)
            elif text_lowercase == 'booking':
                message.command_booking(event, self.line_bot_api, golf_club=golf_club, membership=membership)
            elif text_lowercase in ['course', 'club']:
                message.command_course(event, self.line_bot_api, golf_club=golf_club, membership=membership)
            elif text_lowercase in ['promotions', 'promotion']:
                message.command_promotions(event, self.line_bot_api, golf_club=golf_club, membership=membership)
            elif text_lowercase in ['deals', 'deal', 'hot']:
                message.command_deals(event, self.line_bot_api, golf_club=golf_club, membership=membership)
            elif text_lowercase in ['coupons', 'coupon']:
                message.command_coupons(event, self.line_bot_api, golf_club=golf_club, membership=membership)

            elif text_lowercase in ['location', 'map']:
                message.command_location(event, self.line_bot_api, golf_club=golf_club, membership=membership)
            elif text_lowercase in ['caddies', 'caddie']:
                message.command_caddies(event, self.line_bot_api, golf_club=golf_club, membership=membership)
            elif text_lowercase == 'layout':
                layout = self.request.build_absolute_uri(f'{golf_club.layout.url}')
                message.command_layout(event, self.line_bot_api, layout=layout,
                                       golf_club=golf_club, membership=membership)
            elif text_lowercase in ['hotels', 'hotel', 'accommodation', 'accommodations']:
                message.command_hotels(event, self.line_bot_api, golf_club=golf_club, membership=membership)
            elif text_lowercase in ['restaurants', 'restaurant', 'food']:
                message.command_restaurants(event, self.line_bot_api, golf_club=golf_club, membership=membership)
            else:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(
                        text='What do you want to do?',
                        quick_reply=models.QuickReply(
                            items=[
                                models.QuickReplyButton(action=models.MessageAction(label='My Booking',
                                                                                    text='Booking')),
                            ])))

        @self.handler.add(models.PostbackEvent)
        def handle_post_back(event):
            qs = dict(parse_qsl(event.postback.data))

            cache_key = f'chatbot.membership({event.source.user_id},{golf_club.id})'
            cache_time = settings.CACHES['default']['TIMEOUT86400']

            membership = cache.get(cache_key)

            # Retrieve LINE user
            if not membership:
                try:
                    membership = golf_models.LineUserMembership.objects \
                        .select_related('line_user', 'customer_group') \
                        .get(line_user__line_user_id=event.source.user_id,
                             customer_group__golf_club=golf_club)
                    cache.set(cache_key, membership, cache_time)
                except golf_models.LineUserMembership.DoesNotExist:
                    self.line_bot_api.reply_message(
                        event.reply_token,
                        models.TextSendMessage(text='Invalid Golf Course or LINE ID'))
                    return

            if qs['action'] == 'accept':
                post_back.command_accept(event, self.line_bot_api, qs=qs, golf_club=golf_club, membership=membership)
            elif qs['action'] == 'close':
                post_back.command_close(event, self.line_bot_api, qs=qs, golf_club=golf_club, membership=membership)

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

            if settings.DEBUG:
                log = WebhookRequestLog()
                log.request_header = request.headers
                log.request_body = body
                log.save()

            try:
                self.handler.handle(body, signature)
            except InvalidSignatureError:
                return http.HttpResponseForbidden()

            return http.HttpResponse('OK')

        return http.HttpResponseForbidden()
