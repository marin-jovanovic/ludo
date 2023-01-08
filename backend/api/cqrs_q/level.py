from backend.api.cqrs_q.user import get_users_in_level


def is_level_full_when_this_user_will_be_added_by_id(level_id):
    r = level_get_model_by_id(level_id)
    if not r["status"]:
        return r

    game_o = r["payload"]
    capacity = game_o.capacity

    r = get_users_in_level(level_id)
    if r["status"]:
        currently_active_players = len(r["payload"])
    else:
        print("err get users")
        return r

    return {"status": True, "payload": capacity <= currently_active_players}


def is_level_full_when_this_user_will_be_added(game_name):
    print("not implemented ok is_level_full_when_this_user_will_be_added")
    return

    r = level_get_model_by_id(game_name)
    if not r["status"]:
        return r

    game_o = r["payload"]
    capacity = game_o.capacity

    r = get_users_in_level(game_name)
    if r["status"]:
        currently_active_players = len(r["payload"])
    else:
        print("err get users")
        return r

    return {"status": True, "payload": capacity <= currently_active_players}


def is_level_empty_by_id(level_id):
    r = len(
        get_user_model().objects.filter(currently_playing_id=level_id)
    )

    return {"status": True, "payload": not r}


def is_level_empty(game_name):
    """
    for level name find all users that are currently playing it
    """

    r = level_get_model(game_name)
    if r["status"]:
        game_o = r["payload"]
    else:
        print("err get game")
        return r

    r = len(
        get_user_model().objects.filter(currently_playing=game_o)
    )

    return {"status": True, "payload": not r}


from backend.api.model.user import get_user_model
from backend.api.model.level import get_level_model


def level_get_model_by_id(level_id):
    try:
        g_o = get_level_model().objects.get(id=level_id)
        return {"status": True,
                "payload": g_o}

    except get_level_model().DoesNotExist:
        print(f"level not exists {level_id=}")
        return {"status": False}


def level_get_model_by_id(level_id):
    try:
        level_id = int(level_id)
    except ValueError:
        print(f"can not convert level id to int {level_id=}")
        # return {"status": False}

    try:
        g_o = get_level_model().objects.get(id=level_id)
        return {"status": True,
                "payload": g_o}

    except get_level_model().DoesNotExist:
        print(f"level not exists {level_id=}")
        return {"status": False}


def level_get_model(level_name):
    try:
        g_o = get_level_model().objects.get(name=level_name, is_active=True)
        return {"status": True,
                "payload": g_o}

    except get_level_model().DoesNotExist:
        print(f"level not exists {level_name=}")
        return {"status": False}


# def __check_game_name_exists(name):
#     return {
#         "status": True,
#         "payload": get_level_model().objects.filter(name=name).exists()
#     }


def level_get_filter_id(level_id):
    try:
        level_id = int(level_id)
    except ValueError:
        print("level_get_filter_id can not convert level_id to int")
        return {"status": False}

    try:
        g_o = get_level_model().objects.get(id=level_id)
        return {"status": True, "payload": g_o}

    except get_level_model().DoesNotExist:
        print(f"level not exists {level_id=}")
        return {"status": False}


def __get_game(level_name):
    print("err in function __get_game")

    try:
        g_o = get_level_model().objects.get(level_id=level_name, is_active=True)
        return {"status": True,
                "payload": g_o}

    except get_level_model().DoesNotExist:
        print(f"level not exists {level_name=}")
        return {"status": False}


def is_integrity_rule_ok(level_name):
    """
    integrity rule

    return True if name is ok
    """

    return {
        "status": not get_level_model().objects.filter(name=level_name,
                                                       is_active=True).exists(),
    }
