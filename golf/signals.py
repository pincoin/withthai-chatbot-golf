import json
from functools import wraps
from pathlib import Path

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import time
from django.utils import translation

from . import models


def prevent_recursion(func):
    @wraps(func)
    def no_recursion(sender, instance=None, **kwargs):
        if not instance:
            return

        if hasattr(instance, '_dirty'):
            return

        func(sender, instance=instance, **kwargs)

        try:
            instance._dirty = True
            instance.save()
        finally:
            del instance._dirty

    return no_recursion


@receiver(post_save, sender=models.GolfClub)
@prevent_recursion
def golf_club_post_save(sender, instance, **kwargs):
    translation.activate('en')

    if instance.liff:
        with open(Path(settings.BASE_DIR) / 'liff' / 'static' / 'js' / 'liff' / 'json' / 'course.json') \
                as json_file:
            instance.info_flex_message = json.load(json_file)

            instance.info_flex_message['header']['contents'][0]['text'] = instance.title_english
            instance.info_flex_message['hero']['action']['uri'] = instance.website
            instance.info_flex_message['hero']['url'] = f'https://www.withthai.com{instance.thumbnail.url}'
            instance.info_flex_message['body']['contents'][0]['contents'][1]['text'] = instance.get_hole_display()
            instance.info_flex_message['body']['contents'][1]['contents'][1]['text'] = instance.phone
            instance.info_flex_message['body']['contents'][2]['contents'][1]['text'] = instance.fax
            instance.info_flex_message['body']['contents'][3]['contents'][1]['text'] = instance.email
            instance.info_flex_message['body']['contents'][4]['contents'][1]['text'] \
                = '{} - {}'.format(time(instance.business_hour_start, 'H:i'), time(instance.business_hour_end, 'H:i'))
            instance.info_flex_message['body']['contents'][5]['contents'][4]['action']['uri'] \
                = f"https://liff.line.me/{instance.liff['scorecard']['id']}"

    with open(Path(settings.BASE_DIR) / 'liff' / 'static' / 'js' / 'liff' / 'json' / 'order.json') \
            as json_file:
        instance.order_flex_message = json.load(json_file)

    with open(Path(settings.BASE_DIR) / 'liff' / 'static' / 'js' / 'liff' / 'json' / 'no-order.json') \
            as json_file:
        instance.no_order_flex_message = json.load(json_file)

    translation.deactivate()
