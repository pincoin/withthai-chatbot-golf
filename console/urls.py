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

    path('<slug:slug>/line-users/',
         views.LineUserListView.as_view(), name='line-user-list'),

    path('<slug:slug>/line-users/<str:line_user_id>/',
         views.LineUserDetailView.as_view(), name='line-user-detail'),

    path('<slug:slug>/facebook-users/',
         views.FacebookUserListView.as_view(), name='facebook-user-list'),

    path('<slug:slug>/facebook-users/<str:facebook_user_id>/',
         views.FacebookUserDetailView.as_view(), name='facebook-user-detail'),
]
