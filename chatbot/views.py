import linebot
from django.conf import settings
from django.http import (
    HttpResponse, HttpResponseForbidden
)
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from linebot import models
from linebot.exceptions import InvalidSignatureError

from .models import WebhookRequestLog


@method_decorator(csrf_exempt, name='dispatch')
class CallbackView(generic.View):
    line_bot_api = linebot.LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
    handler = linebot.WebhookHandler(settings.LINE_CHANNEL_SECRET)

    def post(self, request, *args, **kwargs):
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

    @handler.add(models.MessageEvent, message=models.TextMessage)
    def handle_message(self, event):
        text = event.message.text.strip()

        if text == 'profile':
            if isinstance(event.source, models.SourceUser):
                profile = self.line_bot_api.get_profile(event.source.user_id)
                self.line_bot_api.reply_message(
                    event.reply_token, [
                        models.TextSendMessage(text='Display name: ' + profile.display_name),
                        models.TextSendMessage(text='Status message: ' + str(profile.status_message))
                    ]
                )
            else:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    models.TextSendMessage(text="Bot can't use profile API without user ID"))
        elif text == 'quota':
            quota = self.line_bot_api.get_message_quota()
            self.line_bot_api.reply_message(
                event.reply_token, [
                    models.TextSendMessage(text='type: ' + quota.type),
                    models.TextSendMessage(text='value: ' + str(quota.value))
                ]
            )
        elif text == 'quota_consumption':
            quota_consumption = self.line_bot_api.get_message_quota_consumption()
            self.line_bot_api.reply_message(
                event.reply_token, [
                    models.TextSendMessage(text='total usage: ' + str(quota_consumption.total_usage)),
                ]
            )
        elif text == 'push':
            self.line_bot_api.push_message(
                event.source.user_id, [
                    models.TextSendMessage(text='PUSH!'),
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
                    models.TextSendMessage(text='Number of sent broadcast messages: ' + date),
                    models.TextSendMessage(text='status: ' + str(result.status)),
                    models.TextSendMessage(text='success: ' + str(result.success)),
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
                    models.PostbackAction(label='ping with text', data='ping', text='ping'),
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
                    models.PostbackAction(label='ping with text', data='ping', text='ping'),
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
                                action=models.PostbackAction(label="label1", data="data1")
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
                    models.TextSendMessage(text='link_token: ' + link_token_response.link_token)
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

    @handler.add(models.FollowEvent)
    def handle_follow(self, event):
        # event.source.user_id as followed
        self.line_bot_api.reply_message(
            event.reply_token, models.TextSendMessage(text='Got follow event')
        )

    @handler.add(models.UnfollowEvent)
    def handle_unfollow(self, event):
        # event.source.user_id mark as unfollowed
        pass

    @handler.add(models.JoinEvent)
    def handle_join(self, event):
        # event.source.user_id mark as joined
        self.line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text='Joined this ' + event.source.type)
        )

    @handler.add(models.LeaveEvent)
    def handle_leave(self, event):
        # event.source.user_id mark as left
        pass

    @handler.add(models.MemberJoinedEvent)
    def handle_member_joined(self, event):
        self.line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text='Got memberJoined event. event={}'.format(event))
        )

    @handler.add(models.MemberLeftEvent)
    def handle_member_left(event):
        # event.source.user_id mark as left
        pass
