from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    path, include
)

from . import views

urlpatterns = [
    path('',
         views.HomeView.as_view(), name='home'),

    path('chatbot/',
         include('chatbot.urls', namespace='chatbot')),

    path('golf/',
         include('golf.urls', namespace='golf')),

    path('liff/',
         include('liff.urls', namespace='liff')),

    path('console/',
         include('console.urls', namespace='console')),

    path('member/',
         include('member.urls', namespace='member')),

    path('accounts/',
         include('allauth.urls')),

    path('admin/', admin.site.urls),

    path('i18n/',
         include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
