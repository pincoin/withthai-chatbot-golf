import requests
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


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
def send_notification_line(message):
    url = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
        'Authorization': 'Bearer ' + settings.LINE_NOTIFY_ACCESS_TOKEN,
    }
    requests.post(url, data=payload, headers=headers)
