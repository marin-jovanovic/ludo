from backend.api.cqrs_q.users import get_users_in_level


def __is_game_full_when_this_user_will_be_added(game_name):
    r = __get_game(game_name)
    if r["status"]:
        game_o = r["payload"]
    else:
        print("err get game")
        return r

    capacity = game_o.capacity

    r = get_users_in_level(game_name)
    if r["status"]:
        currently_active_players = len(r["payload"])
    else:
        print("err get users")
        return r

    print(f"{capacity=} {currently_active_players=}")
    return {"status": True, "payload": capacity < currently_active_players}


def __check_game_name_exists(name):
    return {
        "status": True,
        "payload": _get_level_model().objects.filter(name=name).exists()
    }


def __is_empty(game_name):
    r = __get_game(game_name)
    if r["status"]:
        game_o = r["payload"]
    else:
        print("err get game")
        return r

    r = len(
        get_user_model().objects.filter(currently_playing=game_o)
    )

    return {"status": True, "payload": not r}


from django.apps import apps
from backend.api.model.player import get_user_model
from backend.api.model.level import _get_level_model


def __get_game(game_name):
    try:
        return {"status": True,
                "payload":
                    _get_level_model().objects.get(name=game_name, is_active=True)}
    except _get_level_model().DoesNotExist:
        return {"status": False, "payload": "game not exist"}
