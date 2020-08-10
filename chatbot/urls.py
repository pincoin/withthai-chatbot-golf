from django.urls import re_path

from . import views

app_name = 'chatbot'

urlpatterns = [
    re_path(r'^(?P<slug>[-\w]+)/callback$',
            views.CallbackView.as_view(), name='callback'),
    re_path(r'^(?P<slug>[-\w]+)/liff/$',
            views.LiffView.as_view(), name='liff-index'),
]
