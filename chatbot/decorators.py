from functools import wraps

from django.utils import translation


def translation_activate(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        translation.activate(kwargs['membership'].line_user.lang)
        func(*args, **kwargs)
        translation.deactivate()

    return decorated
