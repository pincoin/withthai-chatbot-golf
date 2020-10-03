from django.urls import path

from . import views

app_name = 'liff'

urlpatterns = [
    path('<slug:slug>/sample/',
         views.SampleView.as_view(), name='sample'),

    path('<slug:slug>/request/<str:lang>/',
         views.GolfBookingCreateFormView.as_view(), name='request'),

    path('<slug:slug>/settings/<str:lang>/',
         views.GolfBookingSettingsFormView.as_view(), name='settings'),

    path('<slug:slug>/price/<str:lang>/',
         views.GolfPriceTableTemplateView.as_view(), name='price'),

    path('<slug:slug>/scorecard/<str:lang>/',
         views.GolfScorecardTemplateView.as_view(), name='scorecard'),
]
