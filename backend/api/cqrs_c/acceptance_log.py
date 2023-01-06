import json

from backend.api.cqrs_q.level import level_get_model_by_id
from backend.api.model.acceptance_log import \
    acceptance_log_entry_created_notifier
from backend.api.model.acceptance_log import get_acceptance_log_model
from backend.api.model.level import get_level_model
from backend.api.model.level_log import get_level_log_model
from backend.api.model.player_order import get_player_order_model
from backend.api.model.user import get_user_model
from backend.api.cqrs_q.level_log import get_last_performed_by_all_users


def create_entry_if_not_exists(level_id, entry_id, username):
    # test id
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

    r = get_user_model().objects.filter(username=username).exists()
    if not r:
        print(f"[err] {username=}")
        return {
            "status": False
        }

    user_id = get_user_model().objects.get(username=username)

    # skip if entry already in db
    r = get_acceptance_log_model().objects.filter(
        log_entry_id=entry_id,
        user=user_id,
    ).exists()

    if r:
        check_all_accepted(entry_id, level_id)

        return {
            "status": True
        }

    r = get_acceptance_log_model().objects.filter(
        log_entry_id=entry_id,
    ).exists()

    is_first_time = not r
    print(f"{is_first_time=}")

    # are_any_rows_present = get_player_order_model() \
    #     .objects \
    #     .filter(level_id=level_id, user_id=user_id)\
    #     .exists()


    # print("is first entry", t)


    join_index = get_player_order_model() \
        .objects \
        .get(level_id=level_id, user_id=user_id).join_index

    # for this instruction -> player index
    who_can_create_entry_first = get_level_log_model() \
        .objects \
        .get(id=entry_id) \
        .player

    r = level_get_model_by_id(level_id)
    if not r["status"]:
        return r


    # todo
    mode = "fast"
    mode = "slow"

    if mode == "fast":
        acceptance_log = get_acceptance_log_model()

        e = acceptance_log(
            level_id=level_id,
            log_entry_id=entry_id,
            user=user_id,
            accepted=True
        )
        e.save()

        return {
            "status": True
        }

    else:

        # todo
        #   notify only if choosable

        if who_can_create_entry_first == join_index:
            print("index match, must go first")

            if is_first_time:
                print("all good")

                acceptance_log = get_acceptance_log_model()

                e = acceptance_log(
                    level_id=level_id,
                    log_entry_id=entry_id,
                    user=user_id,
                    accepted=True
                )
                e.save()

                msg = json.dumps({
                    "type": "first",
                    "entryId": e.log_entry.id,
                    "id": e.log_entry.instruction_id
                })
                acceptance_log_entry_created_notifier.notify(msg)

                return {
                    "status": True
                }

            else:
                print("err 1 -----------------------------------")

        else:
            print("must no go first")

            if not is_first_time:
                print("all good")

                acceptance_log = get_acceptance_log_model()
                e = acceptance_log(
                    level_id=level_id,
                    log_entry_id=entry_id,
                    user=user_id,
                    accepted=True
                )
                e.save()

                check_all_accepted(entry_id, level_id)

                # max_ = get_last_performed_by_all_users(level_id)

                # if ()

                # if max = this rule

                # msg = json.dumps({
                #     # "type": "maybeLast",
                #     # "lastExecutedAccepted": max_,
                #     # "entryId": e.log_entry.id,
                #     # "id": e.log_entry.instruction_id
                # })
                # acceptance_log_entry_created_notifier.notify(msg)

                # t = is_entry_accepted(level_id, entry_id)
                #
                #
                # print("max accedpt", t)

                # todo if everyone accepted then log as accepted

                return {
                    "status": True
                }


            else:
                print("err 2 -----------------------------------")

        return {
            "status": False
        }


def check_all_accepted(entry_id, level_id):
    print(80 * "+")
    print("already in db")
    r = get_acceptance_log_model().objects \
        .filter(level_id=level_id, log_entry_id=entry_id).count()
    print("total nwo", r)
    capacity = get_level_model().objects.get(id=level_id).capacity
    print(f"{capacity=}")
    if capacity == r:
        print("everyone confirmed")

        q = get_level_log_model().objects.get(id=entry_id)
        q.performed = True
        q.save()

        #    send message that this entry is performed by all

        msg = json.dumps({
            "type": "last",
            "entryIndex": q.instruction_id,
            "entryId": entry_id
            # "lastExecutedAccepted": max_,
            # "entryId": e.log_entry.id,
            # "id": e.log_entry.instruction_id
        })
        acceptance_log_entry_created_notifier.notify(msg)

    else:
        print("missing", capacity - 1, "users to confirm this command")


def is_entry_accepted(level_id, entry_id):
    print(80 * "-")
    capacity = get_level_model().objects.get(id=level_id).capacity
    print(f"{capacity=}")
    num_of_entries_for_this_entry = get_acceptance_log_model() \
        .objects.filter(level_id=level_id, log_entry_id=entry_id).count()
    print(f"{num_of_entries_for_this_entry=}")
    t = capacity == num_of_entries_for_this_entry
    return t
