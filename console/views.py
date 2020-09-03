from django.views import generic

from golf import models as golf_models


class HomeView(generic.TemplateView):
    template_name = 'console/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context


class GolfBookingOrderListView(generic.ListView):
    template_name = 'console/golf_booking_order_list.html'

    context_object_name = 'orders'

    def get_queryset(self):
        return golf_models.GolfBookingOrder.objects \
            .select_related('customer_group') \
            .filter(golf_club__slug=self.kwargs['slug']) \
            .order_by('-round_date', 'round_time')

    def get_context_data(self, **kwargs):
        context = super(GolfBookingOrderListView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context


class GolfBookingOrderDetailView(generic.TemplateView):
    template_name = 'console/golf_booking_order_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GolfBookingOrderDetailView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context
