from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.model.user import get_user_model
from backend.api.view.comm import get_auth_ok_response_template
from backend.api.model.player_order import get_player_order_model
from backend.api.model.level_log import get_level_log_model

class StatisticsView(APIView):
    """
    middleware handles business logic
    """

    def get(self, request, user_id=None):
        """
        return empty payload
        logic handled in middleware
        """

        # find all games that this user played
        levels = get_player_order_model().objects.filter(
            user_id=request.user_id
        ).values("level_id_id", "join_index")

        for lev in levels:
            print(lev)

            r = get_level_log_model().objects.filter(
                action="won",
                game_id=lev["level_id_id"]
            ).order_by("id").values()

            is_found = False
            c = 0
            for i in list(r):
                print(i)
                if i["player"] == lev["join_index"]:
                    print("match")
                    is_found = True
                    break
                c += 1

            new_t = get_player_order_model().objects.get(
                user_id=request.user_id,
                level_id_id=lev["level_id_id"]
            )
            if is_found:
                new_t.index_won=c
                new_t.save()
            else:
                new_t.index_left=1
                new_t.save()


        response = get_auth_ok_response_template(request)

        # if user_id:


        # r = get_user_model().objects.get(id=user_id)

        r = get_player_order_model().objects.filter(
            user_id=request.user_id,
        )

        print(f"{r=}")

        number_of_played_levels = r.count()

        from collections import defaultdict
        wins = defaultdict(list)
        quits = 0
        for i in r:
            if i.index_won:
                wins[i.index_won].append(i.level_id.id)
            else:
                quits += 1

        for i in {0: 3, 1: 2, 2: 3, 3: 1, 4: 0, 5:2}.items():
            wins[i[1]].append(i[0])

        # left =

        levels_played = {}
        for i in r:
            print(f"{i=}")
            levels_played[i.level_id.id] = {"played": True,
                                            "name": i.level_id.name}
        # print(f"{r=}")

        response["payload"] = {
            "status": True,
            "id": request.user_id,
            "username": request.username,
            # "currentlyPlaying": r.currently_playing,
            "numberOfPlayedLevels": number_of_played_levels,
            "wins": wins,
            "levelsPlayed": levels_played,
            "quits": quits
        }

        return JsonResponse(response)

        # else:
        #     print("user view")
        #
        #
        #
        #     return JsonResponse(response)

    # def post(self, user_id):
    #     print("send ")
