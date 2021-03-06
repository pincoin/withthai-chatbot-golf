from django.utils import translation

from golf import models as golf_models


class LiffContextMixin:
    def dispatch(self, request, *args, **kwargs):
        self.golf_club = golf_models.GolfClub.objects.get(slug=self.kwargs['slug'])

        request.LANG = 'en'

        if self.kwargs['lang'] in ['en', 'th', 'ko', 'cn', 'jp']:
            request.LANG = self.kwargs['lang']
            self.liff_id = self.golf_club.liff[self.app_name][request.LANG]['id']

        translation.activate(request.LANG)
        request.LANGUAGE_CODE = request.LANG

        return super(LiffContextMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LiffContextMixin, self).get_context_data(**kwargs)
        context['liffId'] = self.liff_id

        return context
