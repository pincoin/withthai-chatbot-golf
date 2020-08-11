from django.urls import re_path

from . import views

app_name = 'chatbot'

urlpatterns = [
    re_path(r'^(?P<slug>[-\w]+)/sample/$',
            views.SampleView.as_view(), name='sample'),

    re_path(r'^(?P<slug>[-\w]+)/request/$',
            views.BookingCreateFormView.as_view(), name='request'),
]
