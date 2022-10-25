from django.apps import apps
from django.db import models
from backend.api.model.users import get_user_model
from backend.api.model.game import _get_game_model


class GameState(models.Model):
    # primary key
    # id

    # alternate primary key
    # name = models.TextField(unique=True)

    game = models.ForeignKey(
        _get_game_model(),
        on_delete=models.SET_NULL,
        null=True
    )

    current_turn = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True
    )

    # player_order = models.TextField()

    # capacity = models.IntegerField()


# def _get_game_model():
#     return apps.get_model("api.game")


class PlayerOrder(models.Model):

    game_id = models.ForeignKey(_get_game_model(),
                                          on_delete=models.SET_NULL, null=True)

    index = models.IntegerField()
    player = models.ForeignKey(get_user_model(),
                                          on_delete=models.SET_NULL, null=True)

    game_joined_timestamp = models.DateTimeField(auto_now_add=True)

    index_won = models.IntegerField(null=True)

    index_left = models.IntegerField(null=True)


from backend.api.cqrs_q.game import __get_game
from backend.api.cqrs_q.users import get_user

def get_player_order(game_name):
    r = __get_game(game_name)
    if not r["status"]:
        print("get game err")
        return r
    else:
        g_o = r["payload"]

    g = _get_player_order_model().objects.filter(game_id=g_o)
    # for i in g:
    #     print(f"{i.game_id=} {i.index=} {i.player.username=}")

    return {i.index: i.player.username for i in g}

def add_to_order(username, game_name):
    r = __get_game(game_name)
    if not r["status"]:
        print("get game err")
        return r
    else:
        g_o = r["payload"]

    last_index= _get_player_order_model().objects.filter(game_id=g_o)
    max_index = 0
    for i in last_index:
        if i.player.username == username:
            return {"status": False, "debug": "already in add to order"}
        print(i.index, i.player)
        max_index += 1

    r = get_user(username)
    if not r["status"]:
        print("get user err")
        return r
    else:
        u_o = r["payload"]

    g = PlayerOrder(
        game_id=g_o,
        index=max_index,
        player = u_o,
    )
    g.save()

    return {"status": True}
    # pass


def __get_last_index(game_name):
    r = __get_game(game_name)
    if not r["status"]:
        return r
    else:
        g_o = r["payload"]


def set_init_player_order(order):
    print(f"set order {order=}")

def _get_player_order_model():
    return apps.get_model("api.playerorder")
