from django.contrib import admin
from django.urls import (
    path, include
)

urlpatterns = [
    path('chatbot/',
         include('chatbot.urls', namespace='chatbot')),
    
    path('admin/', admin.site.urls),
]
