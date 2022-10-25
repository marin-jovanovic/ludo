from backend.api.cqrs_q.game import __get_game
from backend.api.model.player_order import _get_player_order_model


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
