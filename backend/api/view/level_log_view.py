import urllib

from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from backend.api.cqrs_c.level import create_game, leave_level, join_game, \
    get_active_levels, in_which_level_is_user
from backend.api.model.game_log import game_log_model
from backend.api.view.comm import get_auth_ok_response_template


class LevelLogView(APIView):



    def get(self, request, level_id):
        # get log for this level

        response = get_auth_ok_response_template(request)

        # sort
        log = game_log_model().objects.filter(game_id__name=level_id, game_id__is_active=True)
        print(log)

        for i in log:
            print(i.id, i.instruction_id, i.token, i.dice_result, i.action, i.performed, i.game_id, i.player)

            # json = JSONRenderer().render(i)
            # print(f"{json=}")


        return JsonResponse(response)

    # todo observers


    def post(self, request):
        """
        max 1 active game per player


        """

        # create game

        # creator_username = request.username
        #
        # unquoted_body = urllib.parse.unquote(request.body)
        # body = urllib.parse.parse_qs(unquoted_body)
        #
        # try:
        #     capacity = body["capacity"][0]
        # except KeyError:
        #     capacity = request.data["capacity"]

        print(f"{creator_username=}")
        print(f"{capacity=}")

        response = get_auth_ok_response_template(request)
        # response["payload"] = create_game(creator_username, name, capacity)

        return JsonResponse(response)

    def put(self, request, level_id):
        print(f"{level_id=}")
        # join / leave game
        # username = request.username
        #
        response = get_auth_ok_response_template(request)
        #
        # print(f"{request.data=}")
        #
        # if "leave" in request.data:
        #     response["payload"] = leave_level(name, username)
        #
        # if "join" in request.data:
        #     response["payload"] = join_game(name, username)

        return JsonResponse(response)
