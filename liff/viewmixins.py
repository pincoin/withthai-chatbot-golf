from golf import models as golf_models


class LiffContextMixin:
    def dispatch(self, *args, **kwargs):
        self.golf_club = golf_models.GolfClub.objects.get(slug=self.kwargs['slug'])

        self.liff_id = self.golf_club.liff[self.app_name]['id']

        return super(LiffContextMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LiffContextMixin, self).get_context_data(**kwargs)
        context['liffId'] = self.liff_id

        return context
