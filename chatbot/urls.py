from django.urls import path

from . import views

app_name = 'chatbot'

urlpatterns = [
    path('<slug:slug>/callback/',
         views.CallbackView.as_view(), name='callback'),
]
