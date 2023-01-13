from collections import defaultdict

from backend.api.model.acceptance_log import get_acceptance_log_model
from backend.api.model.level import get_level_model


def get_last_performed_by_all_users(level_id):
    """return entry accepted by all users"""

    capacity = get_level_model().objects.get(id=level_id).capacity

    r = get_acceptance_log_model().objects.filter(level_id=level_id,
                                                  accepted=True).order_by(
        "log_entry_id")

    entry_index_to_rows = defaultdict(list)
    for i in r:
        entry_index_to_rows[i.log_entry.instruction_id].append(i)

    confirmed_entry_index_to_id = {}
    for entry_index, rows in entry_index_to_rows.items():

        if len(rows) == capacity:
            first = rows[0]
            confirmed_entry_index_to_id[entry_index] = first.log_entry_id

    """
    iterate over instruction_id starting from 0
    while instructions are incrementing by one continue
    """

    """test for any entry present"""
    if 0 not in confirmed_entry_index_to_id:
        return {
            "status": False
        }

    """assumption: we can safely return one prev"""
    for e, _ in confirmed_entry_index_to_id.items():
        if e not in confirmed_entry_index_to_id:
            return {
                "status": True,
                "entryIndex": e - 1,
                "entryId": confirmed_entry_index_to_id[e - 1]
            }

    last_index = len(confirmed_entry_index_to_id) - 1

    return {
        "status": True,
        "entryIndex": last_index,
        "entryId": confirmed_entry_index_to_id[last_index]
    }


def get_last_performed_by_this_user(level_id, user_join_index):
    # print(f"{user_join_index=}")

    """return entry accepted by all users"""

    capacity = get_level_model().objects.get(id=level_id).capacity

    r = get_acceptance_log_model().objects.filter(level_id=level_id,
                                                  accepted=True).order_by(
        "log_entry_id")

    entry_index_to_rows = defaultdict(list)
    for i in r:
        entry_index_to_rows[i.log_entry.instruction_id].append(i)

    confirmed_entry_index_to_id = {}
    for entry_index, rows in entry_index_to_rows.items():

        # todo all
        # if len(rows) == capacity:
        #     first = rows[0]
        #     confirmed_entry_index_to_id[entry_index] = first.log_entry_id

        # todo this
        for i in rows:
            if i.user_join_index == user_join_index:
                confirmed_entry_index_to_id[entry_index] = i.log_entry_id
                break

    """
    iterate over instruction_id starting from 0
    while instructions are incrementing by one continue
    """

    """test for any entry present"""
    if 0 not in confirmed_entry_index_to_id:
        return {
            "status": False
        }

    """assumption: we can safely return one prev"""
    for e, _ in confirmed_entry_index_to_id.items():
        if e not in confirmed_entry_index_to_id:
            return {
                "status": True,
                "entryIndex": e - 1,
                "entryId": confirmed_entry_index_to_id[e - 1]
            }

    last_index = len(confirmed_entry_index_to_id) - 1

    return {
        "status": True,
        "entryIndex": last_index,
        "entryId": confirmed_entry_index_to_id[last_index]
    }


def get_any(level_id):
    # print(f"{user_join_index=}")

    """return entry accepted by all users"""

    capacity = get_level_model().objects.get(id=level_id).capacity

    r = get_acceptance_log_model().objects.filter(level_id=level_id,
                                                  accepted=True).order_by(
        "log_entry_id")

    entry_index_to_rows = defaultdict(list)
    for i in r:
        entry_index_to_rows[i.log_entry.instruction_id].append(i)

    confirmed_entry_index_to_id = {}
    for entry_index, rows in entry_index_to_rows.items():

        # todo all
        # if len(rows) == capacity:
        #     first = rows[0]
        #     confirmed_entry_index_to_id[entry_index] = first.log_entry_id

        # todo this
        # for i in rows:
        #     if i.user_join_index == user_join_index:
        #         confirmed_entry_index_to_id[entry_index] = i.log_entry_id
        #         break

        # todo any
        if len(rows) != 0:
            first = rows[0]
            confirmed_entry_index_to_id[entry_index] = first.log_entry_id

    """
    iterate over instruction_id starting from 0
    while instructions are incrementing by one continue
    """

    """test for any entry present"""
    if 0 not in confirmed_entry_index_to_id:
        return {
            "status": False
        }

    """assumption: we can safely return one prev"""
    for e, _ in confirmed_entry_index_to_id.items():
        if e not in confirmed_entry_index_to_id:
            return {
                "status": True,
                "entryIndex": e - 1,
                "entryId": confirmed_entry_index_to_id[e - 1]
            }

    last_index = len(confirmed_entry_index_to_id) - 1

    return {
        "status": True,
        "entryIndex": last_index,
        "entryId": confirmed_entry_index_to_id[last_index]
    }

    #
    # r = get_level_log_model().objects \
    #     .filter(game_id=level_id) \
    #     .annotate(Count("acceptancelog__user")) \
    #     .exclude(acceptancelog__user__count=0) \
    #     .values("instruction_id", "id")\
    #     .order_by("instruction_id")
    #
    # r = list(r)
    #
    # if not r:
    #     print("not r")
    #     return {
    #         "status": False
    #     }
    #
    # max_ = -1
    # for i in r:
    #     if i["instruction_id"] == max_ + 1:
    #         max_ += 1
    #     else:
    #         return {
    #             "status": True,
    #             "entryIndex": i["instruction_id"],
    #             "id": i["id"]
    #         }
    #
    # if max_ == len(r) - 1:
    #     # todo rewrite as last, this is correct but weird
    #     return {
    #         "status": True,
    #         "entryIndex": r[-1]["instruction_id"],
    #         "id": r[-1]["id"]
    #     }
    #
    # print("err")
    # return {
    #     "status": False
    # }
