from django.shortcuts import get_object_or_404
from django.views import generic

from golf import models as golf_models
from .viewmixins import EnglishContextMixin


class HomeView(generic.TemplateView):
    template_name = 'console/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context


class GolfBookingOrderListView(EnglishContextMixin, generic.ListView):
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


class GolfBookingOrderDetailView(EnglishContextMixin, generic.DetailView):
    template_name = 'console/golf_booking_order_detail.html'

    context_object_name = 'order'

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = golf_models.GolfBookingOrder.objects \
            .select_related('customer_group', 'golf_club') \
            .filter(order_no=self.kwargs['uuid'])

        return get_object_or_404(queryset, order_no=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(GolfBookingOrderDetailView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context
