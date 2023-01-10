from backend.api.cqrs_q.level import level_get_model_by_id
from backend.api.model.acceptance_log import \
    notify_all_received, \
    notify_first_received
from backend.api.model.acceptance_log import get_acceptance_log_model
from backend.api.model.level import get_level_model
from backend.api.model.level_log import get_level_log_model
from backend.api.model.player_order import get_player_order_model
from backend.api.model.user import get_user_model

# def check_models_exist(level_id, entry_id, user_id):
#     r = get_level_model().objects.filter(id=level_id).exists()
#     if not r:
#         print(f"[err] {level_id=}")
#         return {
#             "status": False
#         }
#
#     r = get_level_log_model().objects.filter(id=entry_id).exists()
#     if not r:
#         print(f"[err] {entry_id=}")
#         return {
#             "status": False
#         }
#
#     r = get_user_model().objects.filter(id=user_id).exists()
#     if not r:
#         print(f"[err] {user_id=}")
#         return {
#             "status": False
#         }
#
#     return  {
#         "status": True
#     }

def create_entry_if_not_exists(level_id, entry_id, username):
    # r = check_models_exist(level_id, entry_id, user_id)
    # if not r["status"]:
    #     return r

    user_obj = get_user_model().objects.get(username=username)
    user_id = user_obj.id

    # obj, created = get_acceptance_log_model().objects.get_or_create(
    #     level=level_id,
    #     log_entry_id=entry_id,
    #     user=user_id,
    #     defaults={}
    #     # defaults={'birthday': date(1940, 10, 9)},
    # )
    #
    # if not created:
    #     """already exists"""
    #     check_all_accepted(entry_id, level_id, user_id)
    #
    #     return {
    #         "status": True
    #     }


    # skip if entry already in db
    r = get_acceptance_log_model().objects.filter(
        level=level_id,
        log_entry_id=entry_id,
        user=user_id,
    ).exists()

    if r:
        check_all_accepted(entry_id, level_id, user_id)

        return {
            "status": True
        }

    r = get_acceptance_log_model().objects.filter(
        level_id=level_id,
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

    print(f"{e=}")

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

        print("not first")
        check_all_accepted(entry_id, level_id, user_id)

    return {
        "status": True
    }



def check_all_accepted(entry_id, level_id, user_id):

    # removed distinct

    t = get_acceptance_log_model().objects \
        .filter(level_id=level_id, log_entry_id=entry_id)\
        .values("user_id")
    t = list(t)
    print(f"acc l {level_id=} {entry_id=} {user_id=}")
    for e, i in enumerate(t):
        print(e, i)

    r = get_acceptance_log_model().objects \
        .filter(level_id=level_id, log_entry_id=entry_id)\
        .values("user_id").count()

    capacity = get_level_model().objects.get(id=level_id).capacity

    print(f"testing {capacity=} {r=}")
    if capacity == r:
        print("setting performed")

        q = get_level_log_model().objects.get(id=entry_id)
        q.performed = True
        q.save()

        print(f"{q=}")

        t = get_level_log_model().objects.filter(id=entry_id).values()
        t = list(t)
        print(f"{t=}")

        notify_all_received(entry_id, q.instruction_id)

    elif capacity < r:
        print("autofix capacity < r")

        q = get_level_log_model().objects.get(id=entry_id)
        q.performed = True
        q.save()

        notify_all_received(entry_id, q.instruction_id)

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

    # print(80 * "-")
    capacity = get_level_model().objects.get(id=level_id).capacity
    # print(f"{capacity=}")
    num_of_entries_for_this_entry = get_acceptance_log_model() \
        .objects.filter(level_id=level_id, log_entry_id=entry_id).count()
    # print(f"{num_of_entries_for_this_entry=}")
    t = capacity == num_of_entries_for_this_entry
    return t
