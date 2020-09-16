from django.views import generic


class SocialSignUpTestView(generic.TemplateView):
    template_name = 'socialaccount/signup.html'