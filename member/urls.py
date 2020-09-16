from django.urls import path

from . import views

app_name = 'member'

urlpatterns = [
    path('profile/',
         views.SocialSignUpTestView.as_view(), name='profile'),

    path('social-signup-test',
         views.SocialSignUpTestView.as_view(), name='social-sign-up-test-view'),
]
