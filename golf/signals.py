from functools import wraps

from django.db.models.signals import post_save
from django.dispatch import receiver

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


@receiver(post_save, sender=models.LiffApp)
def liff_app_post_save(sender, instance, **kwargs):
    apps = models.LiffApp.objects.filter(golf_club=instance.golf_club)

    app_dict = {}
    for app in apps:
        if app.title not in app_dict:
            app_dict[app.title] = {
                app.lang: {
                    'id': app.app_id,
                    'endpoint_url': app.end_point_url,
                }
            }
        else:
            app_dict[app.title][app.lang] = {
                'id': app.app_id,
                'endpoint_url': app.end_point_url,
            }

    models.GolfClub.objects.filter(slug=instance.golf_club.slug).update(liff=app_dict)
