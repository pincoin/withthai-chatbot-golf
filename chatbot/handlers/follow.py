from linebot import models

from golf import models as golf_models


def command_follow(event, line_bot_api, **kwargs):
    golf_club = kwargs['golf_club']

    try:
        user = golf_models.LineUser.objects.get(line_user_id=event.source.user_id)
    except golf_models.LineUser.DoesNotExist:
        user = golf_models.LineUser()
        user.line_user_id = event.source.user_id

    if isinstance(event.source, models.SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        user.line_display_name = profile.display_name

    user.follow_status = golf_models.LineUser.FOLLOW_CHOICES.follow
    user.fullname = ''
    user.save()

    membership = golf_models.LineUserMembership()
    membership.line_user = user
    membership.customer_group = golf_club.customer_group
    membership.save()

    line_bot_api.reply_message(
        event.reply_token,
        models.TextSendMessage(
            text='Touch the button to send a message.',
            quick_reply=models.QuickReply(
                items=[
                    models.QuickReplyButton(action=models.MessageAction(label='My Booking',
                                                                        text='Booking')),
                ])))
