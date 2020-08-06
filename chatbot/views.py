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

from .models import WebhookLog

line_bot_api = linebot.LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = linebot.WebhookHandler(settings.LINE_CHANNEL_SECRET)


@method_decorator(csrf_exempt, name='dispatch')
class CallbackView(generic.View):
    def post(self, request, *args, **kwargs):
        if 'X-Line-Signature' in request.headers:
            signature = request.headers['X-Line-Signature']
            body = request.body.decode('utf-8')

            log = WebhookLog()
            log.request_header = request.headers
            log.request_body = body
            log.save()

            try:
                handler.handle(body, signature)
            except InvalidSignatureError:
                return HttpResponseForbidden()

            return HttpResponse('OK')

        return HttpResponseForbidden()


@handler.add(models.MessageEvent, message=models.TextMessage)
def handle_message(event):
    text = event.message.text.strip()

    if text == 'profile':
        if isinstance(event.source, models.SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    models.TextSendMessage(text='Display name: ' + profile.display_name),
                    models.TextSendMessage(text='Status message: ' + str(profile.status_message))
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                models.TextSendMessage(text="Bot can't use profile API without user ID"))
    elif text == 'quota':
        quota = line_bot_api.get_message_quota()
        line_bot_api.reply_message(
            event.reply_token, [
                models.TextSendMessage(text='type: ' + quota.type),
                models.TextSendMessage(text='value: ' + str(quota.value))
            ]
        )
    elif text == 'quota_consumption':
        quota_consumption = line_bot_api.get_message_quota_consumption()
        line_bot_api.reply_message(
            event.reply_token, [
                models.TextSendMessage(text='total usage: ' + str(quota_consumption.total_usage)),
            ]
        )
    elif text == 'push':
        line_bot_api.push_message(
            event.source.user_id, [
                models.TextSendMessage(text='PUSH!'),
            ]
        )
    elif text == 'multicast':
        line_bot_api.multicast(
            [event.source.user_id], [
                models.TextSendMessage(text='THIS IS A MULTICAST MESSAGE'),
            ]
        )
    elif text == 'broadcast':
        line_bot_api.broadcast(
            [
                models.TextSendMessage(text='THIS IS A BROADCAST MESSAGE'),
            ]
        )
    elif text.startswith('broadcast '):  # broadcast 20190505
        date = text.split(' ')[1]
        print('Getting broadcast result: ' + date)
        result = line_bot_api.get_message_delivery_broadcast(date)
        line_bot_api.reply_message(
            event.reply_token, [
                models.TextSendMessage(text='Number of sent broadcast messages: ' + date),
                models.TextSendMessage(text='status: ' + str(result.status)),
                models.TextSendMessage(text='success: ' + str(result.success)),
            ]
        )
    elif text == 'bye':
        if isinstance(event.source, models.SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, models.TextSendMessage(text='Leaving group')
            )
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, models.SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, models.TextSendMessage(text='Leaving group')
            )
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                models.TextSendMessage(text="Bot can't leave from 1:1 chat")
            )
    else:
        try:
            line_bot_api.reply_message(
                event.reply_token,
                models.TextSendMessage(text=text)
            )
        except linebot.exceptions.LineBotApiError as e:
            print(e.status_code)
            print(e.request_id)
            print(e.error.message)
            print(e.error.details)


@handler.add(models.FollowEvent)
def handle_follow(event):
    # event.source.user_id as followed
    line_bot_api.reply_message(
        event.reply_token, models.TextSendMessage(text='Got follow event')
    )


@handler.add(models.UnfollowEvent)
def handle_unfollow(event):
    # event.source.user_id mark as unfollowed
    pass


@handler.add(models.JoinEvent)
def handle_join(event):
    # event.source.user_id mark as joined
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='Joined this ' + event.source.type)
    )


@handler.add(models.LeaveEvent)
def handle_leave():
    # event.source.user_id mark as left
    pass


@handler.add(models.MemberJoinedEvent)
def handle_member_joined(event):
    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(text='Got memberJoined event. event={}'.format(event))
    )


@handler.add(models.MemberLeftEvent)
def handle_member_left(event):
    # event.source.user_id mark as left
    pass
