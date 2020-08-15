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
            text = event.message.text.strip()

            if text == 'booking':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='booking list - carousel message'))
            elif text == 'promotions':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='promotions - carousel message'))
            elif text == 'coupons':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='coupons - carousel message'))
            elif text == 'deals':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='deals - carousel message'))
            elif text == 'help':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(
                        text='Quick help commands',
                        quick_reply=models.QuickReply(
                            items=[
                                models.QuickReplyButton(action=models.MessageAction(label='booking',
                                                                                    text='booking')),
                                models.QuickReplyButton(action=models.MessageAction(label='promotions',
                                                                                    text='promotions')),
                                models.QuickReplyButton(action=models.MessageAction(label='coupons',
                                                                                    text='coupons')),
                                models.QuickReplyButton(action=models.MessageAction(label='deals',
                                                                                    text='deals')),
                                models.QuickReplyButton(action=models.MessageAction(label='hotels',
                                                                                    text='hotels')),
                                models.QuickReplyButton(action=models.MessageAction(label='restaurants',
                                                                                    text='restaurants')),
                                models.QuickReplyButton(action=models.MessageAction(label='caddies',
                                                                                    text='caddies')),
                                models.QuickReplyButton(action=models.MessageAction(label='info',
                                                                                    text='info')),
                            ])))
            elif text == 'price':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text='price list - flex or template message'))
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
                        models.LocationSendMessage(title=club.title_english,
                                                   address=club.address,
                                                   latitude=float(club.latitude),
                                                   longitude=float(club.longitude)),
                    ])

            elif text == 'quota':
                quota = self.line_bot_api.get_message_quota()
                self.line_bot_api.reply_message(
                    event.reply_token, [
                        models.TextSendMessage(text=f'type: {quota.type}'),
                        models.TextSendMessage(text=f'value: {str(quota.value)}')
                    ]
                )
            elif text == 'quota_consumption':
                quota_consumption = self.line_bot_api.get_message_quota_consumption()
                self.line_bot_api.reply_message(
                    event.reply_token, [
                        models.TextSendMessage(text=f'total usage: {str(quota_consumption.total_usage)}'),
                    ]
                )
            elif text == 'push':
                self.line_bot_api.push_message(
                    event.source.user_id, [
                        models.TextSendMessage(text='PUSH!'),
                    ]
                )
            elif text == 'location':
                self.line_bot_api.reply_message(
                    event.reply_token, [
                        models.LocationSendMessage(title=club.title_english,
                                                   address=club.address,
                                                   latitude=float(club.latitude),
                                                   longitude=float(club.longitude))
                    ]
                )
            elif text == 'multicast':
                self.line_bot_api.multicast(
                    [event.source.user_id], [
                        models.TextSendMessage(text='THIS IS A MULTICAST MESSAGE'),
                    ]
                )
            elif text == 'broadcast':
                self.line_bot_api.broadcast(
                    [
                        models.TextSendMessage(text='THIS IS A BROADCAST MESSAGE'),
                    ]
                )
            elif text.startswith('broadcast '):  # broadcast 20190505
                date = text.split(' ')[1]
                print('Getting broadcast result: ' + date)
                result = self.line_bot_api.get_message_delivery_broadcast(date)
                self.line_bot_api.reply_message(
                    event.reply_token, [
                        models.TextSendMessage(text=f'Number of sent broadcast messages: {date}'),
                        models.TextSendMessage(text=f'status: {str(result.status)}'),
                        models.TextSendMessage(text=f'success: {str(result.success)}'),
                    ]
                )
            elif text == 'bye':
                if isinstance(event.source, models.SourceGroup):
                    self.line_bot_api.reply_message(
                        event.reply_token, models.TextSendMessage(text='Leaving group')
                    )
                    self.line_bot_api.leave_group(event.source.group_id)
                elif isinstance(event.source, models.SourceRoom):
                    self.line_bot_api.reply_message(
                        event.reply_token, models.TextSendMessage(text='Leaving group')
                    )
                    self.line_bot_api.leave_room(event.source.room_id)
                else:
                    self.line_bot_api.reply_message(
                        event.reply_token,
                        models.TextSendMessage(text="Bot can't leave from 1:1 chat")
                    )
            elif text == 'confirm':
                confirm_template = models.ConfirmTemplate(text='Do it?', actions=[
                    models.MessageAction(label='Yes', text='Yes!'),
                    models.MessageAction(label='No', text='No!'),
                ])
                template_message = models.TemplateSendMessage(
                    alt_text='Confirm alt text', template=confirm_template)
                self.line_bot_api.reply_message(event.reply_token, template_message)
            elif text == 'buttons':
                buttons_template = models.ButtonsTemplate(
                    title='My buttons sample', text='Hello, my buttons', actions=[
                        models.URIAction(label='Go to line.me', uri='https://line.me'),
                        models.PostbackAction(label='ping', data='ping'),
                        models.PostbackAction(label='ping with text', data='ping', display_text='ping'),
                        models.MessageAction(label='Translate Rice', text='米')
                    ])
                template_message = models.TemplateSendMessage(
                    alt_text='Buttons alt text', template=buttons_template)
                self.line_bot_api.reply_message(event.reply_token, template_message)
            elif text == 'carousel':
                carousel_template = models.CarouselTemplate(columns=[
                    models.CarouselColumn(text='hoge1', title='fuga1', actions=[
                        models.URIAction(label='Go to line.me', uri='https://line.me'),
                        models.PostbackAction(label='ping', data='ping')
                    ]),
                    models.CarouselColumn(text='hoge2', title='fuga2', actions=[
                        models.PostbackAction(label='ping with text', data='ping', display_text='ping'),
                        models.MessageAction(label='Translate Rice', text='米')
                    ]),
                ])
                template_message = models.TemplateSendMessage(
                    alt_text='Carousel alt text', template=carousel_template)
                self.line_bot_api.reply_message(event.reply_token, template_message)
            elif text == 'image_carousel':
                image_carousel_template = models.ImageCarouselTemplate(columns=[
                    models.ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                               action=models.DatetimePickerAction(label='datetime',
                                                                                  data='datetime_postback',
                                                                                  mode='datetime')),
                    models.ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                               action=models.DatetimePickerAction(label='date',
                                                                                  data='date_postback',
                                                                                  mode='date'))
                ])
                template_message = models.TemplateSendMessage(
                    alt_text='ImageCarousel alt text', template=image_carousel_template)
                self.line_bot_api.reply_message(event.reply_token, template_message)
            elif text == 'quick_reply':
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(
                        text='Quick reply',
                        quick_reply=models.QuickReply(
                            items=[
                                models.QuickReplyButton(
                                    action=models.PostbackAction(label="label1", data="action=buy&item=111")
                                ),
                                models.QuickReplyButton(
                                    action=models.MessageAction(label="label2", text="text2")
                                ),
                                models.QuickReplyButton(
                                    action=models.DatetimePickerAction(label="label3",
                                                                       data="data3",
                                                                       mode="date")
                                ),
                                models.QuickReplyButton(
                                    action=models.CameraAction(label="label4")
                                ),
                                models.QuickReplyButton(
                                    action=models.CameraRollAction(label="label5")
                                ),
                                models.QuickReplyButton(
                                    action=models.LocationAction(label="label6")
                                ),
                            ])))
            elif text == 'link_token' and isinstance(event.source, models.SourceUser):
                link_token_response = self.line_bot_api.issue_link_token(event.source.user_id)
                self.line_bot_api.reply_message(
                    event.reply_token, [
                        models.TextSendMessage(text=f'link_token: {link_token_response.link_token}')
                    ]
                )
            else:
                try:
                    self.line_bot_api.reply_message(
                        event.reply_token,
                        models.TextSendMessage(text=text)
                    )
                except linebot.exceptions.LineBotApiError as e:
                    print(e.status_code)
                    print(e.request_id)
                    print(e.error.message)
                    print(e.error.details)

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
