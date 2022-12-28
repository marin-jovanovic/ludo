import json

from backend.api.cqrs_q.game import __get_game
from backend.api.cqrs_q.users import get_user, get_users_in_level
from backend.api.model.game_log import GameLog
from backend.api.model.message import Message, message_notifier
from backend.api.model.model_getters import _get_message_model, _get_game_model, \
    _get_player_order_model
from backend.api.model.player import get_user_model


def is_any_entry_present(game):
    r = __get_game(game)
    if r["status"]:
        game_o = r["payload"]
    else:
        return r
    try:
        any_entries = GameLog.objects.filter(game=game_o)

        if bool(any_entries):
            return {"status": True, "payload": True}
        else:
            return {"status": True, "payload": False}

        # print(f"{any_entries=}")

        # print(bool(any_entries), )

        # .exists()
    except GameLog.DoesNotExist:
        return {"status": True, "payload": False}
        # any_entries = None

    # print(f"{any_entries=}")


def get_entries(game):
    r = __get_game(game)
    if r["status"]:
        game_o = r["payload"]
    else:
        return r
    try:
        any_entries = GameLog.objects.filter(game=game_o)
        # .exists()
        return {"status": True, "payload": {i.instruction_id:
            {
                "username": i.player.username,
                "token": i.token,
                "diceResult": i.dice_result,
                "action": i.action,
                "performed": i.performed
            }

            for i in any_entries
        }}
    except GameLog.DoesNotExist:
        any_entries = None
        return {"status": False, }

    # print(f"{any_entries=}")


def create_message(sender, game, content):
    print("create message")
    # print("")

    r = get_user(sender)
    if not r["status"]:
        return r

    else:
        print(r)
        user_o = r["payload"]

    r = __check_game_name_exists(game)
    if not r["payload"]:
        return {"status": False, "payload": "gamen ot exist"}

    r = __get_game(game)
    if not r["payload"]:
        # print(r)
        # print("r payload prsnet")
        return {"status": False, "payload": "game not exiswt"}
    else:
        game_o = r["payload"]

    g = Message(
        game=game_o,
        sender=user_o,
        content=content,
        # timestamp=
    )
    g.save()

    # print("game created", g.name, g.capacity)

    msg = json.dumps({
        "source": "msg created",
        "game": g.game.name,

        "timestamp": str(g.timestamp),
        "sender": g.sender.username,
        "content": g.content

    })

    print(f"{msg=}")

    # game_created_notifier.notify(msg)
    message_notifier.notify(msg)

    print("message created")

    return {"status": True}

    # return __assign_user_currently_playing(creator_username, name)


def get_messages(game):
    r = __check_game_name_exists(game)
    if not r["payload"]:
        return {"status": False, "payload": "gamen ot exist"}

    r = __get_game(game)
    if not r["payload"]:
        # print(r)
        # print("r payload prsnet")
        return {"status": False, "payload": "game not exiswt"}
    else:
        game_o = r["payload"]

    # r = {}
    r = []
    for i in _get_message_model().objects.filter(game=game_o).order_by(
            'timestamp'):
        # print(i.timestamp)
        # print(i.sender)
        # print(i.content)

        r.append({"timestamp": str(i.timestamp), "sender": i.sender.username,
                  "content": i.content})

    return {"status": True, "payload": r}


def __is_game_full(game_name):
    r = __get_game(game_name)
    if r["status"]:
        game_o = r["payload"]
    else:
        return r

    capacity = game_o.capacity

    r = get_users_in_level(game_name)
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


def get_player_order(game_name):
    print("search game", game_name)
    r = __get_game(game_name)
    if not r["status"]:
        print("get game err")
        return r
    else:
        g_o = r["payload"]

    t = _get_player_order_model().objects.filter(game_id=g_o)
    r = {}
    for i in t:
        print(i.join_index, i.player.username)
        r[i.join_index] = i.player.username

    return {"status": True, "payload": r}
