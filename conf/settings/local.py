from django.utils.translation import ugettext_lazy as _

from .base import *

# Internationalization
LANGUAGE_CODE = 'en-US'
LANGUAGES = [
    ('ko', _('Korean')),
    ('th', _('Thai')),
    ('en', _('English')),
]
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'Asia/Bangkok'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')
STATICFILES_DIRS = [
    '/home/ubuntu/.pyenv/versions/withthai/lib/python3.8/site-packages/django/contrib/admin/static',
    os.path.join(BASE_DIR, 'conf', 'static'),
    os.path.join(BASE_DIR, 'allauth', 'static'),
    os.path.join(BASE_DIR, 'liff', 'static'),
    os.path.join(BASE_DIR, 'console', 'static'),
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    # 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Media files (Uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Email reports
ADMINS = [('devops', 'dev@withthai.com'), ]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'golf': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'hotel': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'chatbot': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'liff': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}
