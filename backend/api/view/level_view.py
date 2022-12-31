import urllib

from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.game import create_game, leave_level, join_game, \
    get_levels, in_which_level_is_user
from backend.api.view.comm import get_auth_ok_response_template


class LevelView(APIView):

    def delete(self, request, name=None):
        """
        can not delete level if there are users in it
        when level is empty or only this user is in it -> level can be deleted


        level.active = False
            level will not be shown in get method
            statistics can be created

        this is called when user wants to delete a level
        or
        when level is done

        """

    def get(self, request, name=None):
        # get basic game info

        # todo get in chunks (e.g. 10 by 10 with index and total number of pages in res)
        # todo add filters

        print("get games")

        if name:
            raise NotImplementedError

        else:

            response = get_auth_ok_response_template(request)

            r = get_levels()
            if r["status"]:
                response['payload']["levels"] =r["payload"]
            else:
                response["payload"]["status"] = False
                return JsonResponse(response)

            r = in_which_level_is_user(request.username)
            if r["status"]:
                response["payload"]["inLevel"] = r["payload"]
            else:
                response["payload"]["status"] = False
                return JsonResponse(response)

            response["payload"]["status"] = True

        return JsonResponse(response)

    # todo observers


    def post(self, request, name):
        """
        max 1 active game per player


        """

        # create game

        creator_username = request.username

        unquoted_body = urllib.parse.unquote(request.body)
        body = urllib.parse.parse_qs(unquoted_body)

        try:
            capacity = body["capacity"][0]
        except KeyError:
            capacity = request.data["capacity"]

        print(f"{creator_username=}")
        print(f"{capacity=}")

        response = get_auth_ok_response_template(request)
        response["payload"] = create_game(creator_username, name, capacity)

        return JsonResponse(response)

    def put(self, request, name):
        # join / leave game
        username = request.username

        response = get_auth_ok_response_template(request)

        print(f"{request.data=}")

        if "leave" in request.data:
            response["payload"] = leave_level(name, username)

        if "join" in request.data:
            response["payload"] = join_game(name, username)

        return JsonResponse(response)
