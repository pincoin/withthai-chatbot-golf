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
]
