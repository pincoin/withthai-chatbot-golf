import json
import logging

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
                models.QuickReplyButton(action=models.MessageAction(label='Price List',
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
        club = golf_models.GolfClub.objects.get(slug=self.kwargs['slug'])
        self.logger.info(club.title_english)

        self.line_bot_api = linebot.LineBotApi(club.line_bot_channel_access_token)
        self.handler = linebot.WebhookHandler(club.line_bot_channel_secret)

        @self.handler.add(models.MessageEvent, message=models.TextMessage)
        def handle_message(event):
            text = event.message.text.strip().lower()

            '''
            Rich menu messages
            booking, price, course, promotions, deals(or coupons), settings
            '''
            if text == 'booking':
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
                    models.TextSendMessage(text='price list - flex or template message',
                                           quick_reply=models.QuickReply(
                                               items=[
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='New Booking',
                                                                                   text='New')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Promotions',
                                                                                   text='Promotions')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Hot Deals',
                                                                                   text='Deals')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Coupons',
                                                                                   text='Coupons')),
                                               ])))
            elif text in ['course', 'club']:
                contents = json.loads(club.info)

                contents['header']['contents'][0]['text'] = club.title_english
                contents['hero']['action']['uri'] = club.website
                contents['body']['contents'][0]['contents'][1]['text'] = club.phone
                contents['body']['contents'][1]['contents'][1]['text'] = club.fax

                self.line_bot_api.reply_message(
                    event.reply_token, [
                        models.FlexSendMessage(
                            alt_text=club.title_english,
                            contents=contents,
                            quick_reply=models.QuickReply(
                                items=[
                                    models.QuickReplyButton(
                                        action=models.MessageAction(label='Location',
                                                                    text='Location')),
                                    models.QuickReplyButton(
                                        action=models.MessageAction(label='Caddies',
                                                                    text='Caddies')),
                                    models.QuickReplyButton(
                                        action=models.MessageAction(label='Layout',
                                                                    text='Layout')),
                                    models.QuickReplyButton(
                                        action=models.MessageAction(label='Hotels',
                                                                    text='Hotels')),
                                    models.QuickReplyButton(
                                        action=models.MessageAction(label='Restaurants',
                                                                    text='Restaurants')),
                                ]))
                    ])
            elif text in ['promotions', 'promotion']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='promotions - carousel message',
                                           quick_reply=models.QuickReply(
                                               items=[
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='New Booking',
                                                                                   text='New')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Hot Deals',
                                                                                   text='Deals')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Coupons',
                                                                                   text='Coupons')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Price List',
                                                                                   text='Price')),
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
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Promotions',
                                                                                   text='Promotions')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Coupons',
                                                                                   text='Coupons')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Price List',
                                                                                   text='Price')),
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
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Promotions',
                                                                                   text='Promotions')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Hot Deals',
                                                                                   text='Deals')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Price List',
                                                                                   text='Price')),
                                               ])))
            elif text in ['settings', 'profile']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='settings - carousel message'))

            elif text in ['location', 'map']:
                self.line_bot_api.reply_message(
                    event.reply_token, [
                        models.LocationSendMessage(title=club.title_english,
                                                   address=club.address,
                                                   latitude=float(club.latitude),
                                                   longitude=float(club.longitude),
                                                   quick_reply=models.QuickReply(
                                                       items=[
                                                           models.QuickReplyButton(
                                                               action=models.MessageAction(label='Course',
                                                                                           text='Course')),
                                                           models.QuickReplyButton(
                                                               action=models.MessageAction(label='Caddies',
                                                                                           text='Caddies')),
                                                           models.QuickReplyButton(
                                                               action=models.MessageAction(label='Layout',
                                                                                           text='Layout')),
                                                           models.QuickReplyButton(
                                                               action=models.MessageAction(label='Hotels',
                                                                                           text='Hotels')),
                                                           models.QuickReplyButton(
                                                               action=models.MessageAction(label='Restaurants',
                                                                                           text='Restaurants')),
                                                       ])
                                                   )])
            elif text in ['caddies', 'caddie']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='caddies - carousel message',
                                           quick_reply=models.QuickReply(
                                               items=[
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Course',
                                                                                   text='Course')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Location',
                                                                                   text='Location')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Layout',
                                                                                   text='Layout')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Hotels',
                                                                                   text='Hotels')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Restaurants',
                                                                                   text='Restaurants')),
                                               ])))
            elif text == 'layout':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='layout - carousel message',
                                           quick_reply=models.QuickReply(
                                               items=[
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Course',
                                                                                   text='Course')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Location',
                                                                                   text='Location')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Caddies',
                                                                                   text='Caddies')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Hotels',
                                                                                   text='Hotels')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Restaurants',
                                                                                   text='Restaurants')),
                                               ])))
            elif text in ['hotels', 'hotel', 'accommodation', 'accommodations']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='hotels - carousel message',
                                           quick_reply=models.QuickReply(
                                               items=[
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Course',
                                                                                   text='Course')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Location',
                                                                                   text='Location')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Caddies',
                                                                                   text='Caddies')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Layout',
                                                                                   text='Layout')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Restaurants',
                                                                                   text='Restaurants')),
                                               ])))
            elif text in ['restaurants', 'restaurant', 'food']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='restaurants - carousel message',
                                           quick_reply=models.QuickReply(
                                               items=[
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Course',
                                                                                   text='Course')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Location',
                                                                                   text='Location')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Caddies',
                                                                                   text='Caddies')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Layout',
                                                                                   text='Layout')),
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='Hotels',
                                                                                   text='Hotels')),
                                               ])))

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
                user = golf_models.LineUser.objects.get(line_user_id=event.source.user_id, golf_club=club)
            except golf_models.LineUser.DoesNotExist:
                user = golf_models.LineUser()
                user.line_user_id = event.source.user_id

            if isinstance(event.source, models.SourceUser):
                profile = self.line_bot_api.get_profile(event.source.user_id)
                user.line_display_name = profile.display_name

            user.golf_club = club
            user.follow_status = golf_models.LineUser.FOLLOW_CHOICES.follow
            user.fullname = ''
            user.save()

            self.line_bot_api.reply_message(
                event.reply_token,
                models.TextSendMessage(
                    text='Touch the button to send a message.',
                    quick_reply=self.help_quick_replies))

        @self.handler.add(models.UnfollowEvent)
        def handle_unfollow(event):
            try:
                user = golf_models.LineUser.objects.get(line_user_id=event.source.user_id, golf_club=club)
                user.follow_status = golf_models.LineUser.FOLLOW_CHOICES.unfollow
                user.fullname = ''
                user.save()
            except golf_models.LineUser.DoesNotExist:
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
