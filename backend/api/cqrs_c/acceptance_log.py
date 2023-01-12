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


def get_capacity(level_id):
    capacity  = get_level_model().objects.get(        id=level_id).capacity
    return capacity

def create_entry_if_not_exists(level_id, entry_id, username):

    """aggressive assumption: models exist"""

    user_obj = get_user_model().objects.get(username=username)
    user_id = user_obj.id

    level_id = int(level_id)
    entry_id = int(entry_id)

    user_join_index = get_player_order_model().objects.get(
        level_id=level_id,
        user_id=user_id
    ).join_index

    print(f"{level_id=} {entry_id=} {username=} {user_join_index=}")

    r = get_acceptance_log_model().objects.get(
        log_entry_id=entry_id,
        user_join_index=user_join_index,
    ).accepted

    print(f'is accepted by this user alredy {r=}')

    if r:
        print('already accepted')

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

    r = get_acceptance_log_model().objects.filter(
        log_entry_id=entry_id,
        user_join_index=user_join_index,
    ).values()
    r = list(r)
    print('this acc entry', r)

    my_acceptance_entry = get_acceptance_log_model().objects.get(
        log_entry_id=entry_id,
        user_join_index=user_join_index,
    )

    is_master = my_acceptance_entry.is_first

    # if master and trying to set acceptance not first -> log err and return
    # if not master and trying to set acceptance first -> log err and return

    if is_master:
        print("im master")
        # print('can set accepted for this entry')

        """no checking if already set or
        setting after another user set"""

        my_acceptance_entry.accepted = True
        my_acceptance_entry.save()

        print('set accepted (master)')

        entry_index = my_acceptance_entry.log_entry.instruction_id

        notify_first_received(
            entry_id=entry_id,
            entry_index=entry_index,
            user_join_index=None,
            user_username=username,
            user_id=None
        )

    else:
        print("im slave")
        # print('can not set accepted for this entry')

        # check if master set accepted
        r = get_acceptance_log_model().objects.get(
            log_entry_id=entry_id,
            is_first=True
            # user_join_index=user_join_index,
        ).accepted

        if r:
            print('master accepted, now i can')
            my_acceptance_entry.accepted = True
            my_acceptance_entry.save()

            check_all_accepted(entry_id, level_id)

        else:
            print('err master not accepted, waiting')

    return {
        "status": True
    }



def check_all_accepted(entry_id, level_id):
    r = get_acceptance_log_model().objects.filter(
        log_entry_id=entry_id,
        accepted=True
    ).values()
    r = list(r)

    print(f"{entry_id=} {level_id=} {r=}")

    r = get_acceptance_log_model().objects.filter(
        log_entry_id=entry_id,
        accepted=True
    ).count()



    capacity = get_capacity(level_id)
    if capacity == r:

        r = get_acceptance_log_model().objects.filter(
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
