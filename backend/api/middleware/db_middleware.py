import base64
import urllib

from decouple import config
from django.db.models import Count
from django.http import JsonResponse

from backend.api.comm.comm import get_empty_response_template
from backend.api.cqrs_c.users import create_user, auth_user
from backend.api.cqrs_q.user import is_access_token_correct
from backend.api.model.level_log import get_level_log_model
from backend.api.model.level import get_level_model

class DbMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        self.debug = config("DEBUG") != "0"


    def __call__(self, request):
        # print()

        # print("db mw")

        # print(f"{request.META=}")

        active_levels = get_level_model().objects.filter(
            is_active=True
        )

        for i in active_levels:
            capacity = i.capacity
            level_id = i.id

            #
            get_level_log_model() \
                .objects \
                .filter(game_id=level_id) \
                .annotate(Count("acceptancelog__user")) \
                .filter(acceptancelog__user__count__gte=capacity, performed=False) \
                .update(performed=True)


        return self.get_response(request)
