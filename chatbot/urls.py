from django.urls import re_path

from . import views

app_name = 'chatbot'

urlpatterns = [
    re_path(r'^callback/(?P<slug>[-\w]+)/$',
            views.CallbackView.as_view(), name='callback'),
]
