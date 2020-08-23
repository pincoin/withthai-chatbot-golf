from django.urls import re_path

from . import views

app_name = 'chatbot'

urlpatterns = [
    re_path(r'^(?P<slug>[-\w]+)/sample/$',
            views.SampleView.as_view(), name='sample'),

    re_path(r'^(?P<slug>[-\w]+)/request/$',
            views.GolfBookingCreateFormView.as_view(), name='request'),

    # User
    # Create - request
    # Update - accept
    # Read - list / detail
    # Delete - drop

    # Golf club manager
    # Update - confirm / offer
    # Read - list / detail
    # Delete - no

    re_path(r'^(?P<slug>[-\w]+)/price/$',
            views.GolfPriceTableTemplateView.as_view(), name='price'),

    re_path(r'^(?P<slug>[-\w]+)/scorecard/$',
            views.GolfScorecardTemplateView.as_view(), name='scorecard'),
]
