from golf import models as golf_models


def command_unfollow(event, line_bot_api, **kwargs):
    golf_club = kwargs['golf_club']

    try:
        user = golf_models.LineUser.objects.get(line_user_id=event.source.user_id)
        user.follow_status = golf_models.LineUser.FOLLOW_CHOICES.unfollow
        user.fullname = ''
        user.save()

        membership = golf_models.LineUserMembership.objects \
            .select_related('line_user', 'customer_group') \
            .get(line_user__line_user_id=event.source.user_id,
                 customer_group__golf_club=golf_club)
        membership.delete()
    except (golf_models.LineUser.DoesNotExist, golf_models.LineUserMembership.DoesNotExist):
        pass
