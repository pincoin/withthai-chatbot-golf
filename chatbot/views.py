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
    line_bot_api.reply_message(event.reply_token, models.TextSendMessage(text=event.message.text))
