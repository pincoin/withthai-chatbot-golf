from django.urls import (
    re_path, path
)

from . import views

app_name = 'console'

urlpatterns = [
    path('',
         views.HomeView.as_view(), name='home'),

    re_path(r'^(?P<slug>[-\w]+)/orders/$',
            views.GolfBookingOrderListView.as_view(), name='golf-booking-order-list'),

    re_path(r'^(?P<slug>[-\w]+)/orders/<uuid:uuid>/$',
            views.GolfBookingOrderDetailView.as_view(), name='golf-booking-order-detail'),
]
