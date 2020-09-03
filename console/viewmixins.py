from django.utils import translation


class EnglishContextMixin(object):
    def dispatch(self, request, *args, **kwargs):
        print(self.request)
        translation.activate('en')
        self.request.LANGUAGE_CODE = 'en'
        return super(EnglishContextMixin, self).dispatch(request, *args, **kwargs)
