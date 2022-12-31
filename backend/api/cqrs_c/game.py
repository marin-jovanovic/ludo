import json

from django.apps import apps

from backend.api.cqrs_c.game_log import add_entry
from backend.api.cqrs_c.player_order import add_to_order
from backend.api.cqrs_c.users import make_user_game_creator, \
    make_user_available_to_play, __make_user_join
from backend.api.cqrs_q.game import __is_game_full_when_this_user_will_be_added, __check_game_name_exists, \
    __is_empty, __get_game
from backend.api.cqrs_q.users import get_user, get_users_in_level

from backend.api.model.level import Level, \
    game_created_notifier, games_notifier, game_left_notifier, \
    game_join_notifier, _get_level_model, is_integrity_rule_ok
from backend.api.model.game_log import GameLog
from backend.api.model.c_q import is_any_entry_present, get_entries, \
    get_player_order
from backend.api.model.model_getters import _get_player_order_model
from backend.api.model.player import get_user_model


def create_game(creator_username, name, capacity):
    """
    model users
        set game_role
        set currently_playing_id

    model level
    * create new

    player order
    * do sth

    """

    print("create game")

    capacity = int(capacity)
    if capacity <= 1:
        print("err capacity <= 1")
        return {"status": False, "payload": "capacity must be greater than 1"}

    r = get_user(creator_username)
    if not r["status"]:
        print("err no user")
        return r

    r = is_integrity_rule_ok(name)
    if not r["status"]:
        print("err integrity rule")
        return {"status": False, "payload": "duplicate live level name"}

    r = make_user_game_creator(creator_username)
    if not r["status"]:
        print("err user creator err")
        return r

    g = Level(name=name, capacity=capacity)
    g.save()
    print("game created")

    # todo model: player order
    # r = add_to_order(creator_username, name)
    # if not r["status"]:
    #     return r

    msg = json.dumps({
        "source": "game created",
        "name": g.name,
        "capacity": g.capacity
    })

    print( __is_game_full_when_this_user_will_be_added(name))

    game_created_notifier.notify(msg)
    games_notifier.notify(json.dumps(get_levels()))

    return __assign_user_currently_playing(creator_username, name)


def leave_level(game_name, username):
    r = make_user_available_to_play(username)
    if not r["status"]:
        print("leave_game err make_user_available_to_play")
        return r

    r = __free_user_currently_playing(username)
    if not r["status"]:
        print("leave_game err __free_user_currently_playing")
        return r

    r = __is_empty(game_name)
    if r["status"]:
        f_is_empty = r["payload"]
    else:
        print("leave_game err __is_empty")
        return r

    if f_is_empty:
        print("leave_game level is empty")

        level = _get_level_model().objects.get(name=game_name, is_active=True)
        level.is_active = False
        level.save()

    msg = json.dumps(
        {"source": "leave game", "name": game_name, "who left": username})
    game_left_notifier.notify(msg)
    games_notifier.notify(json.dumps(get_levels()))
    return {"status": True}


def join_game(game_name, username):


    r = add_to_order(username, game_name)
    if not r["status"]:
        print("err add_to_order")
        return r

    r = __get_game(game_name)
    if not r["status"]:
        print("err get game")
        return r

    r = __is_game_full_when_this_user_will_be_added(game_name)
    if not r["status"]:
        print("err __is_game_full")
        return r

    # logic

    r = __make_user_join(username)
    if not r["status"]:
        print("err __make_user_join")
        return r

    r = __assign_user_currently_playing(username, game_name)
    if not r["status"]:
        print("err __assign_user_currently_playing")
        return r

    msg = json.dumps(
        {"source": "join game", "name": game_name, "who joined": username})
    game_join_notifier.notify(msg)
    games_notifier.notify(json.dumps(get_levels()))

    return r


def receive_instruction(game_id, instruction_id):
    r = __get_game(game_id)
    if not r["status"]:
        return r
    else:
        game_o = r["payload"]

    if instruction_id == "test":
        from backend.api.game.game import generate_whole_game

        # todo hardcoded
        g = generate_whole_game()

        r = __add_to_log(game_id, g)
        if not r["status"]:
            return r
        # print("test")

    elif instruction_id == 'generatestart':
        from backend.api.game.game import generate_start

        # todo hardcoded
        g = generate_start()

        r = __add_to_log(game_id, g)
        if not r["status"]:
            return r

    else:
        print(f'other instruction {instruction_id=}')
        # for logging that they user performed this action
        pass

        # GameLog. \
        #     objects. \
        #     filter(
        #     game=game_o,
        #     instruction_id=instruction_id
        # ). \
        #     update(performed=True)

    # todo check all in log if not

    is_any_performed_false = GameLog.objects.filter(performed=False,
                                                    game_id=game_o)
    # print(f"{is_any_performed_false=}")

    if is_any_performed_false:
        print("not last instruciton, required user action")
    else:
        print("last instruction, generate new")



    return {"status": True}


def __add_to_log(game_id, order):
    r = __get_game(game_id)
    if not r["status"]:
        return r

    try:
        g_o = _get_level_model().objects.get(name=game_id)
    except _get_level_model().DoesNotExist:
        return {"status": False}

    for i in order:

        if i["action"] == "roll":
            i["performed"] = False
        else:
            i["performed"] = True

        i["game"] = game_id

        t = _get_player_order_model().objects.get(
            game_id=g_o,
            join_index=i["player"]
        )

        i["player"] = t.player.username
        # print(i)

        add_entry(**i)

        # r = add_entry(**i)
        # print("result add", r)

    return {"status": True}


def get_specific_game(game_id):
    try:
        g_o = _get_level_model().objects.get(name=game_id)
    except _get_level_model().DoesNotExist:
        return {"status": False}

    r = get_users_in_level(g_o.name)
    if r["status"]:
        pass
        # currently_active_players = r["payload"]
    else:
        return r

    r = is_any_entry_present(game=game_id)
    if r["status"]:
        r = r["payload"]
    else:
        return r

    # generate start rolls, determine order
    # if not r:
    #
    #     game_conf = get_config()
    #
    #     order = determine_order(
    #         g_o.capacity,
    #         # game_conf['number of players'],
    #         game_conf['choice: highest; order'],
    #         game_conf['choice: clockwise; anticlockwise'],
    #         game_conf['flag: tie in order'],
    #     )
    #
    #     turn = 0
    #     for i in order:
    #
    #         if i["action"] == "goes":
    #             _get_player_order_model().objects.filter(
    #                 game_id=g_o,
    #                 join_index=i["player"]
    #             ).update(turn_index=turn)
    #
    #             turn += 1
    #
    #     r = __add_to_log(game_id, order)
    #     if not r["status"]:
    #         return r

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


def get_levels():

    levels = {}

    for c, level in enumerate(_get_level_model().objects.all()):

        r = get_users_in_level(level.name)

        if r["status"]:
            users_in_level = r["payload"]
        else:
            return r

        users_in_level = [
            i.username for i in users_in_level
        ]

        levels[c] = {
            "id": level.id,
            "capacity": level.capacity,
            "players": users_in_level
        }

    return {
        "status": True,
        "payload": levels
    }


def in_which_level_is_user(username):
    r = get_user_model().objects.get(username=username).currently_playing_id

    try:
        g = _get_level_model().objects.get(id=r).name
    except _get_level_model().DoesNotExist:
        # request is performed but user is not in any game
        # so status is true
        g = None

    return {"status": True, "payload": g}


def __delete_game(name):
    return {"status": False, "debug": "can not delete in this impl"}

    # if __check_game_name_exists(name):
    #     return {
    #         "status": True,
    #         "payload": _get_level_model().objects.filter(name=name).delete()
    #     }
    #
    # return {"status": False, "debug": "game not exist"}


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

