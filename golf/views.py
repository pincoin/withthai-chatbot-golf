from django.http import JsonResponse
from django.views import generic


class GolfClubFeeJson(generic.TemplateView):
    def render_to_response(self, context, **response_kwargs):
        data = {
            'club': {},
            'rates': [],
            'holidays': [],
        }

        return JsonResponse(
            data,
            json_dumps_params={'ensure_ascii': False},
            **response_kwargs
        )


class GolfClubScorecardJson(generic.TemplateView):
    def render_to_response(self, context, **response_kwargs):
        data = {
        }

        return JsonResponse(
            data,
            json_dumps_params={'ensure_ascii': False},
            **response_kwargs
        )
