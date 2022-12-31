from backend.api.cqrs_q.level import __get_game
from backend.api.cqrs_q.users import get_user
from backend.api.model.player_order import PlayerOrder
from backend.api.model.model_getters import _get_player_order_model


def player_order_create_entry(username, game_name):
    """


    """

    r = __get_game(game_name)
    if not r["status"]:
        print("get game err")
        return r
    else:
        g_o = r["payload"]

    last_index = _get_player_order_model().objects.filter(game_id=g_o)
    max_index = 0
    for i in last_index:
        if i.player.username == username:
            print("err already in add to order")
            return {"status": False, "debug": "already in add to order"}
        max_index += 1

    r = get_user(username)
    if not r["status"]:
        print("get user err")
        return r
    else:
        u_o = r["payload"]

    g = PlayerOrder(
        game_id=g_o,
        join_index=max_index,
        player=u_o,
    )
    g.save()

    return {"status": True}
