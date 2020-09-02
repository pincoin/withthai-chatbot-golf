from django.views import generic


class HomeView(generic.TemplateView):
    template_name = 'console/home.html'


class GolfBookingOrderListView(generic.TemplateView):
    template_name = 'console/golf_booking_order_list.html'


class GolfBookingOrderDetailView(generic.TemplateView):
    template_name = 'console/golf_booking_order_detail.html'
