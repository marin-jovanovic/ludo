from django.apps import apps
from django.db import models

from backend.api.cqrs_q.game import __get_game
from backend.api.model.game import _get_game_model
from backend.api.model.users import get_user_model


class PlayerOrder(models.Model):

    game_id = models.ForeignKey(_get_game_model(),
                                          on_delete=models.SET_NULL, null=True)

    index = models.IntegerField()
    player = models.ForeignKey(get_user_model(),
                                          on_delete=models.SET_NULL, null=True)

    game_joined_timestamp = models.DateTimeField(auto_now_add=True)

    index_won = models.IntegerField(null=True)

    index_left = models.IntegerField(null=True)


def get_player_order(game_name):
    print("search game", game_name)
    r = __get_game(game_name)
    if not r["status"]:
        print("get game err")
        return r
    else:
        g_o = r["payload"]

    t = PlayerOrder.objects.filter(game_id=g_o)
    r = {}
    for i in t:
        print(i.index, i.player.username)
        r[i.index] = i.player.username
    # t = serializers.serialize('json', [ t, ])
    # print(f"{t=}")
    # import json
    # serialized = json.dumps(dict_obj)
    return {"status": True, "payload": r}


def _get_player_order_model():
    return apps.get_model("api.playerorder")