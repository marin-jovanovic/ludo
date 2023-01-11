import json

from backend.api.cqrs_c.game_log import add_entry
from backend.api.cqrs_c.player_order import player_order_create_entry
from backend.api.cqrs_c.users import make_user_game_creator, \
    make_user_available_to_play, user_set_game_roll_to_join
from backend.api.cqrs_q.level import \
    level_get_model, is_level_empty_by_id, \
    level_get_model_by_id, is_level_full_when_this_user_will_be_added_by_id, \
    is_integrity_rule_ok
from backend.api.cqrs_q.user import get_user, get_users_in_level
# from backend.api.game.main import create_game_api

from backend.api.game.main import create_level

from backend.api.model.level import Level, \
    game_created_notifier, games_notifier, game_left_notifier, \
    game_join_notifier, get_level_model
from backend.api.model.player_order import get_player_order_model
from backend.api.model.user import get_user_model


def in_which_level_is_user(username):
    r = get_user_model().objects.get(username=username).currently_playing_id

    try:
        g = get_level_model().objects.get(id=r).name
    except get_level_model().DoesNotExist:
        # request is performed but user is not in any game
        # so status is true
        g = None

    return {"status": True, "payload": g}


def create_game(creator_username, level_name, capacity):
    """
    model users
        set game_role
        set currently_playing_id

    model level
    * create new

    player order
    * do sth

    """

    capacity = int(capacity)
    if capacity <= 1:
        print("err capacity <= 1")
        return {"status": False, "payload": "capacity must be greater than 1"}

    r = get_user(creator_username)
    if not r["status"]:
        print("err no user")
        return r

    # duplicate live level name
    r = is_integrity_rule_ok(level_name)
    if not r["status"]:
        print("err is_integrity_rule_ok duplicate live level name")
        return {"status": False, "payload": "duplicate live level name"}

    # game_role
    r = make_user_game_creator(creator_username)
    if not r["status"]:
        print("err user creator err")
        return r

    # create level
    g = Level(name=level_name, capacity=capacity)
    g.save()
    # print("level created")

    # player order object
    r = player_order_create_entry(creator_username, g.id)
    if not r["status"]:
        print("err add_to_order")
        return r

    r = level_get_model(level_name=level_name)
    if not r["status"]:
        return r

    game_o = r["payload"]

    level_id = game_o.id

    r =  driver_assign_user_currently_playing(creator_username, game_o, level_id)
    if not r["status"]:
        return r

    from backend.api.cqrs_q.level import level_name_to_level_id
    r = level_name_to_level_id(level_name)
    if not r["status"]:
        return r
    level_id = r["payload"]

    r = create_level(level_id)
    if not r["status"]:
        return r

    log = r["payload"]

    # from backend.api.game.adapter import artificially_add_choose_row
    #
    # log = artificially_add_choose_row(log)

    for i in log:
        i["game"] = level_name

        add_entry(**i)

    from backend.api.model.level_log import get_level_log_model
    from backend.api.model.acceptance_log import get_acceptance_log_model
    acceptance_log_model = get_acceptance_log_model()

    log = get_level_log_model().objects.filter(
        game=level_id
    )

    q = get_player_order_model().objects.filter(level_id_id=level_id).values()
    q = list(q)

    for i in q:
        print(i)


    for entry in log:
        for player_index in range(capacity):
            '''assumption is_first = this.user_join_index == log_entry.player'''

            q = acceptance_log_model(
                level_id=level_id,
                log_entry=entry,
                user_join_index=player_index,
                accepted=False,
                is_first=entry.player==player_index,
            )
            q.save()





    msg = json.dumps({
        "source": "game created",
        "name": g.name,
        "capacity": g.capacity
    })

    game_created_notifier.notify(msg)
    games_notifier.notify(json.dumps(get_active_levels()))

    return {"status": True,
            "levelId": g.id
            }


# def add_new_last_entry(log):
#     last_entry = log[-1]
#     # this fixes "choose" part
#     from backend.api.game.log import user_choose
#     new_last_entry = user_choose(last_entry["player"],
#                                  last_entry["dice_result"])
#     log.append(new_last_entry)


def get_player_order(game_name):
    r = level_get_model(game_name)
    if not r["status"]:
        print("get game err")
        return r
    else:
        g_o = r["payload"]

    t = get_player_order_model().objects.filter(game_id=g_o)
    r = {}
    for i in t:
        print(i.join_index, i.player.username)
        r[i.join_index] = i.player.username

    return {"status": True, "payload": r}


def leave_level(username):
    """level name is obsolete"""

    r = get_user(username)
    if r["status"]:
        user_o = r["payload"]
    else:
        return r

    # todo one player playing multiple levels at same time
    # if not user_o.currently_playing_id == level_id:
    #     print("err  mismatch, does not matter, i can fix that")

    level_id = user_o.currently_playing_id

    print(f"{user_o.game_role=}")

    if not user_o.currently_playing_id and not user_o.game_role:
        print("err user not in any game")
        return {"status": False, "payload": "user not in any level"}

    # check if in this specific level

    try:
        _ = get_user_model().objects.get(username=username,
                                         currently_playing_id=level_id)
    except get_user_model().DoesNotExist:
        print("user not in this level")
        return {"status": False, "payload": "user not in this level"}

    # other checks and logic

    r = make_user_available_to_play(username)
    if not r["status"]:
        print("leave_game err make_user_available_to_play")
        return r

    r = user_clear_currently_playing_id(username)
    if not r["status"]:
        print("leave_game err __free_user_currently_playing")
        return r

    r = is_level_empty_by_id(level_id)
    if r["status"]:
        f_is_empty = r["payload"]
    else:
        print("leave_game err __is_empty")
        return r

    if f_is_empty:
        print("leave_game level is empty")

        level = get_level_model().objects.get(id=level_id)
        level.is_active = False
        level.save()

    # "levelName": "__todo__"
    msg = json.dumps(

        {"source": "leave game", "levelId": level_id, "who left": username})
    game_left_notifier.notify(msg)
    games_notifier.notify(json.dumps(get_active_levels()))
    return {"status": True}


def join_level(level_id, username):
    # todo cleanup for consistency

    # assumption: user in another level
    r = get_user_model().objects.get(username=username)
    # print(f"{r.game_role=}")
    # print(f"{r.currently_playing=}")

    # fixme what if bool(1)
    # this should be fixed with db, not on this level

    # this is quick fix

    if r.game_role and r.currently_playing:
        """assuming both are correct"""

    elif r.game_role and not r.currently_playing:
        """
        if currently_playing is not present ->
        go over all levels and find where this one is present
        """

        r.game_role = None
        r.save()

    elif not r.game_role and r.currently_playing:
        """
        if game_role is not present, I need to find currently_playing
        if creator is present -> game_role = "joined"
        else -> game_role = "creator"
        """

        r.currently_playing = None
        r.save()

    else:
        """
        assumption: nothing is present
        """

    r = level_get_model_by_id(level_id)
    if not r["status"]:
        print("err get game")
        return r

    r = is_level_full_when_this_user_will_be_added_by_id(level_id)
    if not r["status"]:
        print("err __is_game_full")
        return r

    if r["payload"]:
        print("err game full")
        return r

    # logic

    # player order object
    r = player_order_create_entry(username, level_id)
    if not r["status"]:
        return r

    # user object

    r = user_set_game_roll_to_join(username=username)
    if not r["status"]:
        print("err __make_user_join")
        return r

    r = user_set_currently_playing_id(username=username, level_id=level_id)
    if not r["status"]:
        return r

    # other

    msg = json.dumps({
        "source": "join game",
        "who joined": username,
        "levelId": level_id
    })

    game_join_notifier.notify(msg)
    games_notifier.notify(json.dumps(get_active_levels()))

    r["payload"]["levelId"] = level_id

    print(f"{r=}")

    return r


def get_active_levels():
    # perform cleanup

    levels = {}

    for level in get_level_model().objects.all():

        if not level.is_active:
            continue

        r = get_users_in_level(level.id)

        if r["status"]:
            users_in_level = r["payload"]
        else:
            return r

        users_in_level = [
            i.username for i in users_in_level
        ]

        levels[level.id] = {
            "name": level.name,
            "capacity": level.capacity,
            "players": users_in_level,
            "levelId": level.id
        }

    # cleanup
    is_changed = False
    for id_, meta in levels.items():

        if not meta["players"]:
            level = get_level_model().objects.get(id=meta["levelId"])
            level.is_active = False
            level.save()
            is_changed = True

    if is_changed:
        return get_active_levels()

    return {
        "status": True,
        "payload": levels
    }


def user_clear_currently_playing_id(username):
    # todo
    return driver_assign_user_currently_playing(username, None, "todo")


def user_set_currently_playing_id(username, level_id):
    r = level_get_model_by_id(level_id)
    if not r["status"]:
        return r

    game_o = r["payload"]

    return driver_assign_user_currently_playing(username, game_o, level_id)


def driver_assign_user_currently_playing(username, game_o, level_id):
    r = get_user(username)
    if not r["status"]:
        return r

    user_o = r["payload"]
    user_o.currently_playing = game_o
    user_o.save()

    # r["payload"]["levelId"]
    return {"status": True, "payload": {
        "levelId": level_id

    }}
