from django.urls import path

from . import views

app_name = 'console'

urlpatterns = [
    path('<slug:slug>/',
         views.HomeView.as_view(), name='home'),

    path('<slug:slug>/orders/',
         views.GolfBookingOrderListView.as_view(), name='golf-booking-order-list'),

    path('<slug:slug>/orders/<uuid:uuid>/',
         views.GolfBookingOrderDetailView.as_view(), name='golf-booking-order-detail'),

    path('<slug:slug>/orders/<uuid:uuid>/confirm/',
         views.GolfBookingOrderConfirmView.as_view(), name='golf-booking-order-confirm'),

    path('<slug:slug>/orders/<uuid:uuid>/offer/',
         views.GolfBookingOrderOfferView.as_view(), name='golf-booking-order-offer'),

    path('<slug:slug>/orders/<uuid:uuid>/reject/',
         views.GolfBookingOrderRejectView.as_view(), name='golf-booking-order-reject'),
]
