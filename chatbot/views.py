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

        self.buttons_menu_template = models.ButtonsTemplate(
            title='Menu', text='menu', actions=[
                models.PostbackAction(label='New booking', data='new'),
                models.PostbackAction(label='My booking', data='my'),
                models.PostbackAction(label='Price List', data='price'),
                models.PostbackAction(label='Promotion', data='promotion'),
            ])

    def post(self, request, *args, **kwargs):
        club = golf_models.GolfClub.objects.get(slug=self.kwargs['slug'])
        self.logger.info(club.title_english)

        self.line_bot_api = linebot.LineBotApi(club.line_bot_channel_access_token)
        self.handler = linebot.WebhookHandler(club.line_bot_channel_secret)

        @self.handler.add(models.MessageEvent, message=models.TextMessage)
        def handle_message(event):
            text = event.message.text.strip().lower()

            if text == 'booking':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='booking list - carousel message',
                                           quick_reply=models.QuickReply(
                                               items=[
                                                   models.QuickReplyButton(
                                                       action=models.MessageAction(label='New booking',
                                                                                   text='new')),
                                               ])))
            elif text == 'price':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='price list - flex or template message'))
            elif text == 'promotions':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='promotions - carousel message'))
            elif text == 'course':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='course - carousel message'))
            elif text == 'settings':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='settings - carousel message'))

            elif text == 'coupons':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='coupons - carousel message'))
            elif text == 'deals':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='deals - carousel message'))
            elif text == 'hotels':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='hotels - carousel message'))
            elif text == 'restaurants':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='restaurants - carousel message'))
            elif text == 'caddies':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='caddies - carousel message'))
            elif text == 'location':
                self.line_bot_api.reply_message(
                    event.reply_token, [
                        models.LocationSendMessage(title=club.title_english,
                                                   address=club.address,
                                                   latitude=float(club.latitude),
                                                   longitude=float(club.longitude))
                    ]
                )
            elif text == 'info':
                self.line_bot_api.reply_message(
                    event.reply_token, [
                        models.FlexSendMessage(
                            alt_text='hello',
                            contents={
                                'type': 'bubble',
                                'direction': 'ltr',
                                'hero': {
                                    'type': 'image',
                                    'url': 'https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png',
                                    'size': 'full',
                                    'aspectRatio': '20:13',
                                    'aspectMode': 'cover',
                                    'action': {'type': 'uri', 'uri': 'https://www.withthai.com', 'label': 'label'}}}),
                    ])
            else:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(
                        text='Quick help commands',
                        quick_reply=models.QuickReply(
                            items=[
                                models.QuickReplyButton(action=models.MessageAction(label='My Booking',
                                                                                    text='Booking')),
                                models.QuickReplyButton(action=models.MessageAction(label='Price',
                                                                                    text='Price')),
                                models.QuickReplyButton(action=models.MessageAction(label='Promotions',
                                                                                    text='Promotions')),
                                models.QuickReplyButton(action=models.MessageAction(label='Coupons',
                                                                                    text='Coupons')),
                                models.QuickReplyButton(action=models.MessageAction(label='Hot Deals',
                                                                                    text='Deals')),
                                models.QuickReplyButton(action=models.MessageAction(label='Caddies',
                                                                                    text='Caddies')),
                                models.QuickReplyButton(action=models.MessageAction(label='Course Info',
                                                                                    text='Info')),
                                models.QuickReplyButton(action=models.MessageAction(label='Location',
                                                                                    text='Location')),
                                models.QuickReplyButton(action=models.MessageAction(label='Hotels',
                                                                                    text='Hotels')),
                                models.QuickReplyButton(action=models.MessageAction(label='Restaurants',
                                                                                    text='Restaurants')),
                                models.QuickReplyButton(action=models.PostbackAction(label='표시내용',
                                                                                     display_text='보내는내용',
                                                                                     data='명령어')),
                            ])))

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

            template_message = models.TemplateSendMessage(alt_text='Menu', template=self.buttons_menu_template)

            self.line_bot_api.reply_message(event.reply_token, template_message)

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
