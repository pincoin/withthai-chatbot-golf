from django.urls import path

from . import views

app_name = 'golf'

urlpatterns = [
    path('<slug:slug>/fee.json',
         views.GolfClubFeeJson.as_view(), name='fee'),

    path('<slug:slug>/scorecard.json',
         views.GolfClubScorecardJson.as_view(), name='scorecard'),

    path('<slug:slug>/customer-group.json',
         views.GolfClubCustomerGroup.as_view(), name='customer-group'),
]
