from backend.api.cqrs_q.users import get_users_in_level
from backend.api.model.c_q import get_entries


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
    return {"status": True, "payload": capacity <= currently_active_players}



def is_level_empty(game_name):
    """
    for level name find all users that are currently playing it
    """

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

    return level_get_model(game_name)


def level_get_model(level_name):

    try:
        g_o = _get_level_model().objects.get(name=level_name, is_active=True)
        return {"status": True,
                "payload": g_o}

    except _get_level_model().DoesNotExist:
        print(f"level not exists {level_name=}")
        return {"status": False}

