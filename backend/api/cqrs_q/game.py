# from backend.api.cqrs_c.game import _get_game_model
from backend.api.cqrs_q.users import get_users_in_game
# # from backend.api.model.game import _get_game_model
# from backend.api.model.users import get_user_model


def __is_game_full(game_name):
    r = __get_game(game_name)
    if r["status"]:
        game_o = r["payload"]
    else:
        return r

    capacity = game_o.capacity

    r = get_users_in_game(game_name)
    if r["status"]:
        currently_active_players = len(r["payload"])
    else:
        return r

    return {"status": True, "payload": capacity <= currently_active_players}


def __check_game_name_exists(name):
    return {
        "status": True,
        "payload": _get_game_model().objects.filter(name=name).exists()
    }


def __is_empty(game_name):
    r = __get_game(game_name)
    if r["status"]:
        game_o = r["payload"]
    else:
        return r

    r = len(
        get_user_model().objects.filter(currently_playing=game_o)
    )

    return {"status": True, "payload": not r}


from django.apps import apps


def _get_game_model():
    return apps.get_model("api.game")

def get_user_model():
    return apps.get_model("api.Users")


def __get_game(game_name):
    try:
        return {"status": True,
                "payload":
                    _get_game_model().objects.get(name=game_name)}
    except _get_game_model().DoesNotExist:
        return {"status": False, "payload": "game not exist"}
