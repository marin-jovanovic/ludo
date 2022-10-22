import json

from django.apps import apps
from django.db import models

from backend.api.cqrs_c.users import make_user_available_to_play
from backend.api.cqrs_c.users import make_user_game_creator, __make_user_join
from backend.api.cqrs_q.users import get_user, get_users_in_game
from backend.api.model.users import get_user_model

from backend.api.comm.comm import Notifier
# games_notifier = Notifier()

game_created_notifier = Notifier()
game_left_notifier = Notifier()
game_join_notifier = Notifier()
games_notifier = Notifier()
class Game(models.Model):
    # primary key
    # id

    # alternate primary key
    name = models.TextField(unique=True)

    capacity = models.IntegerField()


def create_game(creator_username, name, capacity):
    print("create game")
    capacity = int(capacity)
    if capacity <= 1:
        return {"status": False, "payload": "capacity must be greater than 1"}

    r = get_user(creator_username)
    if not r["status"]:
        return r

    r = make_user_game_creator(creator_username)
    if not r["status"]:
        return r

    r = __check_game_name_exists(name)
    if r["payload"]:
        return {"status": False, "payload": "duplicate game name"}

    g = Game(name=name, capacity=capacity)
    g.save()

    print("game created", g.name, g.capacity)

    msg = json.dumps({
        "source": "game created",
        "name": g.name, "capacity": g.capacity})

    game_created_notifier.notify(msg)
    games_notifier.notify(json.dumps(get_games()))

    return __assign_user_currently_playing(creator_username, name)


def leave_game(game_name, username):
    r = make_user_available_to_play(username)
    if r["status"]:
        pass
    else:
        print("err make_user_available_to_play")
        return r

    r = __free_user_currently_playing(username)
    if r["status"]:
        pass
    else:
        print("err __free_user_currently_playing")
        return r

    r = __is_empty(game_name)
    if r["status"]:
        f_is_empty = r["payload"]
    else:
        print("err __is_empty")
        return r

    if f_is_empty:
        print("is empty")
        __delete_game(game_name)

    msg = json.dumps({"source": "leave game","name": game_name, "who left": username})
    game_left_notifier.notify(msg)
    games_notifier.notify(json.dumps(get_games()))
    return {"status": True}


def join_game(game_name, username):
    r = __get_game(game_name)
    if not r["status"]:
        return r

    r = __is_game_full(game_name)
    if not r["status"]:
        return {"status": False, "payload": "capacity filled"}

    r = __make_user_join(username)
    if not r["status"]:
        return r

    r = __assign_user_currently_playing(username, game_name)
    if not r["status"]:
        return r

    msg = json.dumps({"source": "join game","name": game_name, "who joined": username})
    game_join_notifier.notify(msg)
    games_notifier.notify(json.dumps(get_games()))

    return r


def get_games():
    full = []
    not_full = []

    for i in _get_game_model().objects.all():

        r = __is_game_full(i.name)
        if r["status"]:
            is_full = r["payload"]
        else:
            return {"status": False, "payload": "get games error"}

        r = __get_game(i.name)
        if not r["status"]:
            return r

        r = get_users_in_game(i.name)
        if r["status"]:
            currently_active_players = r["payload"]
        else:
            return r

        currently_active_players = [i.username for i in
                                    currently_active_players]

        if is_full:
            full.append({"name": i.name, "capacity": i.capacity,
                         "players": currently_active_players})

        else:
            not_full.append({"name": i.name, "capacity": i.capacity,
                             "players": currently_active_players})

    print(f"ret {full=} {not_full=}")
    return {"status": True, "payload": {
        "full": full,
        "not full": not_full
    }}


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


def __delete_game(name):
    if __check_game_name_exists(name):
        return {
            "status": True,
            "payload": _get_game_model().objects.filter(name=name).delete()
        }

    return {"status": False}


def __check_game_name_exists(name):
    return {
        "status": True,
        "payload": _get_game_model().objects.filter(name=name).exists()
    }


def __get_game(game_name):
    try:
        return {"status": True,
                "payload":
                    _get_game_model().objects.get(name=game_name)}
    except _get_game_model().DoesNotExist:
        return {"status": False, "payload": "game not exist"}


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


def __free_user_currently_playing(username):
    return __driver_assign_user_currently_playing(username, None)


def __assign_user_currently_playing(username, game_name):
    r = __get_game(game_name)
    if r["status"]:
        game_o = r["payload"]
    else:
        return r

    return __driver_assign_user_currently_playing(username, game_o)


def __driver_assign_user_currently_playing(username, status):
    r = get_user(username)
    if r["status"]:
        user_o = r["payload"]
    else:
        return r

    user_o.currently_playing = status
    user_o.save()

    return {"status": True}


def _get_game_model():
    return apps.get_model("api.game")
