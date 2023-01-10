from django.db.models import Count

from backend.api.model.level import get_level_model
from backend.api.model.level_log import get_level_log_model
from backend.api.model.acceptance_log import get_acceptance_log_model

def get_last_performed_by_all_users(level_id):

    """return entry accepted by all users"""

    capacity  = get_level_model().objects.get(        id=level_id).capacity

    r = get_level_log_model()\
        .objects \
        .filter(game_id=level_id) \
        .annotate(Count("acceptancelog__user")) \
        .filter(acceptancelog__user__count__gte=capacity) \
        .values("instruction_id", "id")\
        .order_by("id")

    r = list(r)

    if not r:
        print("not is yet accepted (by all)")
        return {
            "status": False
        }

    """
    iterate over instruction_id starting from 0
    while instructions are incrementing by one continue
    """

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

    last = r[-1]

    if max_ == len(r) - 1:
        # todo rewrite as last, this is correct but weird
        return {
            "status": True,
            "entryIndex": last["instruction_id"],
            "id": last["id"]
        }

    print("err get_last_performed_by_all_users")
    return {
        "status": False
    }

def get_last_performed_by_this_user(level_id, user_id):
    # print("get_last_performed_by_this_user")

    r = get_acceptance_log_model().objects\
        .filter(level_id=level_id,user_id=user_id)\
        .values("log_entry__instruction_id", "log_entry_id", ) \
        .order_by("log_entry_id")
    r = list(r)

    # distinct removed

    if not r:
        print(f"not r get_last_performed_by_this_user {r=}")
        return {
            "status": False
        }

    max_ = -1
    for i in r:
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
            "entryIndex": r[-1]["log_entry__instruction_id"],
            "id": r[-1]["log_entry_id"]
        }

    print("err get_last_performed_by_this_user")

    return {
        "status": False
    }


def get_any(level_id):

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
            "entryIndex": r[-1]["instruction_id"],
            "id": r[-1]["id"]
        }

    print("err")
    return {
        "status": False
    }

