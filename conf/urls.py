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

    path('admin/', admin.site.urls),
]
