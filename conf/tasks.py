import linebot
import requests
from celery import shared_task
from django.core.mail import send_mail
from linebot import models


@shared_task
def send_notification_email(subject, message, from_email, recipient, html_message=None):
    send_mail(
        subject,
        message,
        from_email,
        [recipient],
        fail_silently=True,
        html_message=html_message,
    )


@shared_task
def send_notification_line(line_notify_access_token, message):
    url = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
        'Authorization': f'Bearer {line_notify_access_token}',
    }
    requests.post(url, data=payload, headers=headers)


@shared_task
def send_push_text_message_line(line_bot_channel_access_token, to, message, **kwargs):
    quick_reply = None

    if 'postback_actions' in kwargs:
        items = []
        for action in kwargs['postback_actions']:
            items.append(models.QuickReplyButton(
                action=models.PostbackAction(label=action['label'],
                                             data=action['data'],
                                             display_text=action['displayText'])))

        quick_reply = models.QuickReply(items=items)

    line_bot_api = linebot.LineBotApi(line_bot_channel_access_token)
    line_bot_api.push_message(to, models.TextSendMessage(text=message, quick_reply=quick_reply))
