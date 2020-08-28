from django.urls import re_path

from . import views

app_name = 'golf'

urlpatterns = [
    re_path(r'^(?P<slug>[-\w]+)/fee.json$',
            views.GolfClubFeeJson.as_view(), name='fee'),

    re_path(r'^(?P<slug>[-\w]+)/scorecard.json$',
            views.GolfClubScorecardJson.as_view(), name='scorecard'),

    re_path(r'^(?P<slug>[-\w]+)/customer-group.json$',
            views.GolfClubCustomerGroup.as_view(), name='customer-group'),
]
