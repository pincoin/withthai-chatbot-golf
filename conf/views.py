from django.shortcuts import render
from django.views import generic


class HomeView(generic.TemplateView):
    template_name = 'conf/home.html'


def handler404(request, exception):
    # Page not found
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler403(request, exception=None):
    # Permission denied
    response = render(request, '403.html', {})
    response.status_code = 403
    return response


def handler500(request, exception=None):
    # Internal server error
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
