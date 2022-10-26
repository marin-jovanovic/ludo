import json

from backend.api.cqrs_c.users import make_user_game_creator, \
    make_user_available_to_play, __make_user_join
from backend.api.cqrs_q.users import get_user, get_users_in_game

from backend.api.model.game import Game, \
    game_created_notifier, games_notifier, game_left_notifier, \
    game_join_notifier
from backend.api.cqrs_q.game import __is_game_full, __check_game_name_exists, \
    __is_empty, __get_game
from backend.api.cqrs_c.player_order import add_to_order

from backend.api.cqrs_c.game_log import add_entry


def create_game(creator_username, name, capacity):
    print("create game")
    capacity = int(capacity)
    if capacity <= 1:
        return {"status": False, "payload": "capacity must be greater than 1"}

    r = get_user(creator_username)
    if not r["status"]:
        return r

    r = __check_game_name_exists(name)
    if r["payload"]:
        return {"status": False, "payload": "duplicate game name"}

    r = make_user_game_creator(creator_username)
    if not r["status"]:
        return r

    g = Game(name=name, capacity=capacity)
    g.save()

    r = add_to_order(creator_username, name)
    if not r["status"]:
        return r


    # r = add_entry(name, creator_username, None, None, "hello world")
    # if not r["status"]:
    #     return r

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
    r = add_to_order(username, game_name)
    if not r["status"]:
        return r

    r = __get_game(game_name)
    if not r["status"]:
        print("err get game")
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


from backend.api.model.player_order import get_player_order
from backend.api.model.game_log import get_entries, is_any_entry_present, \
    GameLog
from backend.api.game.game import determine_order, get_config
from backend.api.model.player_order import _get_player_order_model
from backend.api.cqrs_c.player_order import add_to_order
from backend.api.model.player_order import get_player_order
from backend.api.model.game_log import get_entries
from django.db.models import Max

def receive_instruction(game_id, instruction_id):
    r = __get_game(game_id)
    if not r["status"]:
        return r
    else:
        game_o = r["payload"]

    if instruction_id == "test":
        print("test")

    else:

        GameLog.\
            objects.\
            filter(
                game=game_o,
                instruction_id=instruction_id
            ).\
            update(performed=True)

    last_performed_instruction = GameLog.objects.filter(performed=True).aggregate(Max('instruction_id'))["instruction_id__max"]
    last_instruction = GameLog.objects.aggregate(Max('instruction_id'))["instruction_id__max"]

    print(f"{last_performed_instruction=}")
    print(f"{last_instruction=}")

    if (last_performed_instruction == last_instruction):
        print("this is last instruciton, generate new")

        last_command = GameLog.objects.get(instruction_id=last_performed_instruction).action
        print(f"{last_command=}")
        if last_command == "goes":
            # todo here
            print("generate board ")

        else:
            pass
            # todo think this can only be choice if user rolled 6

    else:
        print("not last instruction")

    return {"status": True}

def get_specific_game(game_id):
    print(f"{game_id=}")

    try:
        g_o = _get_game_model().objects.get(name=game_id)
    except _get_game_model().DoesNotExist:
        return {"status": False}

    r = get_users_in_game(g_o.name)
    if r["status"]:
        currently_active_players = r["payload"]
    else:
        return r

    for i in currently_active_players:
        print(f"{i.username=} {i.game_role=}")

    r = is_any_entry_present(game=game_id)
    if r["status"]:
        r = r["payload"]
    else:
        return r

    if r:
        print("init roll in db")
    else:
        print("adding init data")

        game_conf = get_config()

        order = determine_order(
            g_o.capacity,
            # game_conf['number of players'],
            game_conf['choice: highest; order'],
            game_conf['choice: clockwise; anticlockwise'],
            game_conf['flag: tie in order'],
        )

        r = __get_game(game_id)
        if not r["status"]:
            return r

        m_join_to_turn_index = {}
        turn = 0
        for i in order:

            if i["action"] == "goes":
                m_join_to_turn_index[i["player"]] = turn

                _get_player_order_model().objects.filter(
                    game_id=g_o,
                    join_index=i["player"]
                ).update(turn_index=turn)

                turn += 1

        for i in order:
            i["game"] = game_id

            t = _get_player_order_model().objects.get(
                game_id=g_o,
                join_index=i["player"]
            )

            i["player"] = t.player.username
            i["performed"] = False
            print(i)

            r = add_entry(**i)
            print("result add", r)

    r = get_entries(game_id)
    if not r["status"]:
        return r
    log = r["payload"]

    return {"status": True,
            "payload": {
                # "name": g_o.name,
                # "capacity": g_o.capacity,
                "players": get_player_order(game_name=game_id),
                # "turn": "a",
                # "action": "tmp_",
                "header": "determination who goes first",

                # game state
                "state": {},
                "creator": "tmp_",
                "log": log
            }
    }


def get_games():
    full = {}
    not_full = {}

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

        g = {
                "name": i.name,
                "capacity": i.capacity,
                "players": currently_active_players
            }

        if is_full:
            full[i.name] = g

        else:
            not_full[i.name] = g

    return {"status": True, "payload": {
        "full": full,
        "not full": not_full,
        # ""
    }}

from backend.api.model.users import get_user_model

def in_which_game_is_user(username):
    # print("usernaem", username)

    r = get_user_model().objects.get(username=username).currently_playing_id
    # print(r)

    try:
        g = _get_game_model().objects.get(id=r).name
    except _get_game_model().DoesNotExist:
        g = None
    # print(g.name)

    return {"status": False, "payload": g}

def __delete_game(name):
    if __check_game_name_exists(name):
        return {
            "status": True,
            "payload": _get_game_model().objects.filter(name=name).delete()
        }

    return {"status": False}


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
from django.apps import apps

def _get_game_model():
    return apps.get_model("api.game")
