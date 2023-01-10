import sys

from backend.api.cqrs_q.level import level_get_model_by_id
from backend.api.model.acceptance_log import \
    notify_all_received, \
    notify_first_received
from backend.api.model.acceptance_log import get_acceptance_log_model
from backend.api.model.level import get_level_model
from backend.api.model.level_log import get_level_log_model
from backend.api.model.player_order import get_player_order_model
from backend.api.model.user import get_user_model

def check_models_exist(level_id, entry_id, user_id):
    r = get_level_model().objects.filter(id=level_id).exists()
    if not r:
        print(f"[err] {level_id=}")
        return {
            "status": False
        }

    r = get_level_log_model().objects.filter(id=entry_id).exists()
    if not r:
        print(f"[err] {entry_id=}")
        return {
            "status": False
        }

    r = get_user_model().objects.filter(id=user_id).exists()
    if not r:
        print(f"[err] {user_id=}")
        return {
            "status": False
        }

    return  {
        "status": True
    }


def get_capacity(level_id):
    capacity  = get_level_model().objects.get(        id=level_id).capacity
    return capacity

def create_entry_if_not_exists(level_id, entry_id, username):

    user_obj = get_user_model().objects.get(username=username)
    user_id = user_obj.id

    level_id = int(level_id)
    entry_id = int(entry_id)

    # print(f"{level_id=} {entry_id=} {user_id=}")

    # todo
    user_join_index =


    # r = get_acceptance_log_model().objects.filter(
    #     level_id=level_id,
    #     log_entry_id=entry_id,
    #     user_join_index=user_join_index,
    # ).values()
    # r = list(r)
    #
    # for i in r:
    #     print(i)

    r = get_acceptance_log_model().objects.get(
        level_id=level_id,
        log_entry_id=entry_id,
        user_join_index=user_join_index,
    ).accepted

    if r:

        """
        this user accepted this entry
        no need for adding
        check if all accepted
        assumption: notif for first entry was sent
        """

        check_all_accepted(entry_id, level_id)

        return {
            "status": True
        }


    # return  {
    #     "status": True
    # }

    # skip if entry already in db
    # r = get_acceptance_log_model().objects.filter(
    #     log_entry_id=entry_id,
    #     user=user_obj,
    # ).exists()
    #
    # if r:
    #     check_all_accepted(entry_id, level_id)
    #
    #     return {
    #         "status": True
    #     }

    # todo
    sys.exit(-1)

    r = get_acceptance_log_model().objects.filter(
        log_entry_id=entry_id,
    ).exists()

    is_first_time = not r

    join_index = get_player_order_model() \
        .objects \
        .get(level_id=level_id, user_id=user_id).join_index

    # for this instruction -> player index
    who_can_create_entry_first = get_level_log_model() \
        .objects \
        .get(id=entry_id) \
        .player

    # todo
    #   notify only if choosable

    if who_can_create_entry_first == join_index:
        if not is_first_time:
            print("err 1 -----------------------------------")

            return {
                "status": False
            }

    else:
        if is_first_time:
            print("err 2 must no go first")

            return {
                "status": False
            }

    acceptance_log = get_acceptance_log_model()
    e = acceptance_log(
        level_id=level_id,
        log_entry_id=entry_id,
        user=user_obj,
        accepted=True
    )
    e.save()

    if who_can_create_entry_first == join_index:


        entry_index = e.log_entry.instruction_id

        notify_first_received(
            entry_id=entry_id,
            entry_index=entry_index,
            user_join_index=None,
            user_username=username,
            user_id=None
        )

    else:

        check_all_accepted(entry_id, level_id)

    return {
        "status": True
    }



def check_all_accepted(entry_id, level_id):
    # r = get_acceptance_log_model().objects \
    #     .filter(level_id=level_id, log_entry_id=entry_id).count()

    r = get_acceptance_log_model().objects.filter(
        level_id=level_id,
        log_entry_id=entry_id,
        accepted=True
    ).count()


    # r = get_acceptance_log_model().objects.filter(
    #     log_entry_id=entry_id,
    #     # user=user_obj,
    # ).exists()

    # r = get_acceptance_log_model().objects \
    #     .filter(level_id=level_id, log_entry_id=entry_id)\
    #     .values("user_id").distinct().count()
    #
    # capacity = get_level_model().objects.get(id=level_id).capacity

    capacity = get_capacity(level_id)
    if capacity == r:

        r = get_acceptance_log_model().objects.filter(
            level_id=level_id,
            log_entry_id=entry_id,
        )

        # todo do this in more elegant way (using native first?)
        for i in r:
            """just pick first"""
            notify_all_received(entry_id, i.log_entry.instruction_id)
            break
    else:
        print("missing", capacity - r, "users to confirm this command")


def is_entry_accepted(level_id: int, entry_id: int) -> bool:
    """
    Check if a given entry has been accepted by all users in a given level.

    Parameters:
    level_id (int): The ID of the level to check.
    entry_id (int): The ID of the entry to check.

    Returns:
    bool: True if the entry has been accepted by all users in the level,
          False otherwise.
    """

    capacity = get_level_model().objects.get(id=level_id).capacity
    num_of_entries_for_this_entry = get_acceptance_log_model() \
        .objects.filter(level_id=level_id, log_entry_id=entry_id).count()
    t = capacity == num_of_entries_for_this_entry
    return t
