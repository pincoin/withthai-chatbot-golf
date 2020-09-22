from django.urls import path

from . import views

app_name = 'chatbot'

urlpatterns = [
    path('<slug:slug>/sample/',
         views.SampleView.as_view(), name='sample'),

    path('<slug:slug>/request/',
         views.GolfBookingCreateFormView.as_view(), name='request'),

    path('<slug:slug>/settings/',
         views.GolfBookingSettingsFormView.as_view(), name='settings'),

    path('<slug:slug>/price/',
         views.GolfPriceTableTemplateView.as_view(), name='price'),

    path('<slug:slug>/scorecard/',
         views.GolfScorecardTemplateView.as_view(), name='scorecard'),
]
