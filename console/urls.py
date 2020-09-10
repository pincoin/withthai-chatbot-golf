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

    path('<slug:slug>/line-users/',
         views.LineUserListView.as_view(), name='line-user-list'),

    path('<slug:slug>/line-users/<str:line_user_id>/',
         views.LineUserDetailView.as_view(), name='line-user-detail'),

    path('<slug:slug>/facebook-users/',
         views.FacebookUserListView.as_view(), name='facebook-user-list'),

    path('<slug:slug>/facebook-users/<str:facebook_user_id>/',
         views.FacebookUserDetailView.as_view(), name='facebook-user-detail'),

    path('<slug:slug>/settings/golf-club/',
         views.GolfClubUpdateView.as_view(), name='golf-club-update'),

    path('<slug:slug>/settings/rates/',
         views.GreenFeeListView.as_view(), name='green-fee-list'),

    path('<slug:slug>/settings/holidays/',
         views.HolidayListView.as_view(), name='holiday-list'),

    path('<slug:slug>/settings/seasons/',
         views.SeasonListView.as_view(), name='season-list'),

    path('<slug:slug>/settings/timeslots/',
         views.TimeslotListView.as_view(), name='timeslot-list'),
]
