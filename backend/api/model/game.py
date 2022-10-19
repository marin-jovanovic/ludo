from django.db import models

# from backend.api.model.users import Users
from backend.api.cqrs_c.users import make_user_game_creator
from backend.api.cqrs_q.users import get_user
from backend.api.model.users import get_user_model
from backend.api.cqrs_c.users import make_user_available_to_play
from django.apps import apps


class Game(models.Model):
    # primary key
    # id

    # alternate primary key
    name = models.TextField(unique=True)

    capacity = models.IntegerField()

    # player


def create_game(creator_username, name, capacity):
    capacity = int(capacity)

    r = get_user(creator_username)
    if not r["status"]:
        print(f"no {creator_username=}")
        return r

    r = make_user_game_creator(creator_username)
    if not r["status"]:
        return r

    r = __check_game_name_exists(name)
    if r["payload"]:
        print(f"duplicate name {name=}")
        return {"status": False, "payload": "duplicate game name"}

    if capacity <= 1:
        return {"status": False, "payload": "capacity must be greater than 1"}

    g = Game(name=name, capacity=capacity)
    g.save()

    return {"status": True, "payload": "game created"}


def leave_game(game_name, username):
    # set to null
    r = make_user_available_to_play(username)
    if r["status"]:
        pass
        # f_is_empty = r["payload"]
    else:
        return r

    r = __is_empty(game_name)
    if r["status"]:
        f_is_empty = r["payload"]
    else:
        return r

    print(f"{f_is_empty=}")

    if f_is_empty:
        __delete_game(game_name)
        print(f"game empty {r}")

    else:
        print("game not empty")

    return {"status": True}


def join_game(game_name, username):
    print(f"join {game_name=} {username=}")
    pass

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
    print(f"get game {game_name=}")
    try:
        return {"status": True,
                "payload":
                    _get_game_model().objects.get(name=game_name)}
    except:
        return {"status": False}


def __is_empty(game_name):
    r = __get_game(game_name)
    if r["status"]:
        game_o = r["payload"]
    else:
        print(r)
        return r

    r = len(
        get_user_model().objects.filter(currently_playing=game_o)
    )

    print("empty count", r)

    return {"status": True, "payload": not r}


def __is_full():
    pass


def __add_user_to_game(username, game_name):
    r = get_user(username)
    if r["status"]:
        user_o = r["payload"]
    else:
        return r

    game_o = __get_game(game_name)

    user_o.currently_playing = game_o
    user_o.save()




def _get_game_model():
    return apps.get_model("api.game")
