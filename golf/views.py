from django.http import JsonResponse
from django.views import generic

from . import models


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


class GolfClubCustomerGroup(generic.TemplateView):
    def render_to_response(self, context, **response_kwargs):
        membership = models.LineUserMembership \
            .objects.get(line_user__line_user_id=self.kwargs['line_user_id'],
                         customer_group__golf_club__slug=self.kwargs['slug'])

        data = {
            'customer_group_id': membership.customer_group_id,
            'customer_group_title_english': membership.customer_group.title_english,
        }

        return JsonResponse(
            data,
            json_dumps_params={'ensure_ascii': False},
            **response_kwargs
        )
