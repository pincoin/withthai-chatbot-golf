from golf import models as golf_models


class LiffContextMixin(object):
    def dispatch(self, *args, **kwargs):
        self.liff = golf_models.Liff.objects.get(golf_club__slug=self.kwargs['slug'], app_name=self.app_name)
        return super(LiffContextMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LiffContextMixin, self).get_context_data(**kwargs)
        context['liffId'] = self.liff.liff_id
        return context
