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

    path('admin/', admin.site.urls),
]
