from django.db.models import Count

from backend.api.model.level import get_level_model
from backend.api.model.level_log import get_level_log_model
from backend.api.model.acceptance_log import get_acceptance_log_model

def get_last_performed_by_all_users(level_id):
    print("get_last_performed_by_all_users")
    r = get_level_log_model().objects \
        .filter(game_id=level_id) \
        .annotate(Count("acceptancelog__user")) \
        .filter(acceptancelog__user__count=get_level_model().objects.get(
        id=level_id).capacity) \
        .values("instruction_id", "id")\
        .order_by("instruction_id")


    r = list(r)

    if not r:
        print("not r")
        return {
            "status": False
        }

    # print("accept: logged by all users")
    for i in r:
        print(i)

    max_ = -1
    for i in r:
        if i["instruction_id"] == max_ + 1:
            max_ += 1
        else:
            return {
                "status": True,
                "entryIndex": i["instruction_id"],
                "id": i["id"]
            }

    if max_ == len(r) - 1:
        # todo rewrite as last, this is correct but weird
        return {
            "status": True,
            "entryIndex": i["instruction_id"],
            "id": i["id"]
        }

    print("err")
    return {
        "status": False
    }

def get_last_performed_by_this_user(level_id, user_id):
    print("get_last_performed_by_this_user")

    r = get_acceptance_log_model().objects\
        .filter(level_id=level_id,user_id=user_id)\
        .values("log_entry__instruction_id", "log_entry_id", ) \
        .order_by("log_entry_id").distinct()

    r = list(r)

    if not r:
        print(f"not r {r=}")
        return {
            "status": False
        }

    for i in r:
        print(i)

    max_ = -1
    for i in r:
        print(f"try {i=} {max_+ 1 =}")
        if i["log_entry__instruction_id"] == max_ + 1:
            max_ += 1
        else:
            return {
                "status": True,
                "entryIndex": i["log_entry__instruction_id"],
                "id": i["log_entry_id"]
            }

    if max_ == len(r) - 1:
        return {
            "status": True,
            "entryIndex": i["log_entry__instruction_id"],
            "id": i["log_entry_id"]
        }

    print("err")

    return {
        "status": False
    }


def get_any(level_id):
    print("get_max_performed_by_any")

    print("get_last_performed_by_all_users")
    r = get_level_log_model().objects \
        .filter(game_id=level_id) \
        .annotate(Count("acceptancelog__user")) \
        .exclude(acceptancelog__user__count=0) \
        .values("instruction_id", "id")\
        .order_by("instruction_id")

    r = list(r)

    if not r:
        print("not r")
        return {
            "status": False
        }

    # print("accept: logged by all users")
    for i in r:
        print(i)

    max_ = -1
    for i in r:
        if i["instruction_id"] == max_ + 1:
            max_ += 1
        else:
            return {
                "status": True,
                "entryIndex": i["instruction_id"],
                "id": i["id"]
            }

    if max_ == len(r) - 1:
        # todo rewrite as last, this is correct but weird
        return {
            "status": True,
            "entryIndex": i["instruction_id"],
            "id": i["id"]
        }

    print("err")
    return {
        "status": False
    }

    # r = get_acceptance_log_model().objects \
    #     .filter(level_id=level_id) \
    #     .values("log_entry__instruction_id", "log_entry_id", ) \
    #     .order_by("log_entry_id")
    #
    #
    # if not r:
    #     print(f"not r {r=}")
    #     return {
    #         "status": False
    #     }
    #
    # for i in r:
    #     print(i)
    #
    # max_ = -1
    # for i in r:
    #     print(f"try {i=} {max_+ 1 =}")
    #     if i["log_entry__instruction_id"] == max_ + 1:
    #         max_ += 1
    #     else:
    #         return {
    #             "status": True,
    #             "entryIndex": i["log_entry__instruction_id"],
    #             "id": i["log_entry_id"]
    #         }
    #
    # if max_ == len(r) - 1:
    #     return {
    #         "status": True,
    #         "entryIndex": i["log_entry__instruction_id"],
    #         "id": i["log_entry_id"]
    #     }
    #
    # print("err")
    #
    # return {
    #     "status": False
    # }
