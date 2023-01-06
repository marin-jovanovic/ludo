# from backend.api.cqrs_q.game import __get_game

from backend.api.model.player_order import get_player_order_model


def get_player_order(game_name):
    r = __get_game(game_name)
    if not r["status"]:
        print("get game err")
        return r
    else:
        g_o = r["payload"]

    g = get_player_order_model().objects.filter(game_id=g_o)
    # for i in g:
    #     print(f"{i.game_id=} {i.index=} {i.player.username=}")

    return {i.index: i.player.username for i in g}


def get_players(level_id):

    from backend.api.model.player_order import get_player_order_model

    r = get_player_order_model().objects.filter(level_id=level_id).values()
    r = list(r)

    ret = {}

    t = {
        '0': {
            'colour': 'green',

        },
        '1': {
            'colour': 'blue',

        },
        '2': {
            'colour': 'yellow',

        },
        '3': {
            'colour': 'red',
        }
    }


    for i, val in enumerate(r):
        ret[str(i)] = {
            "colour": t[str(i)]["colour"],
            'username': get_player_order_model()
            .objects
            .get(level_id=level_id, join_index=val["join_index"]).user.username
        }



    return ret

