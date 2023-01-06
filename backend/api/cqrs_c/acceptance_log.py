import json

from backend.api.cqrs_q.level import level_get_model_by_id
from backend.api.model.acceptance_log import \
    acceptance_log_entry_created_notifier
from backend.api.model.acceptance_log import get_acceptance_log_model
from backend.api.model.level import get_level_model
from backend.api.model.level_log import get_level_log_model
from backend.api.model.player_order import get_player_order_model
from backend.api.model.user import get_user_model


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
        print("already in db")
        return {
            "status": True
        }

    r = get_acceptance_log_model().objects.filter(
        log_entry_id=entry_id,
    ).exists()

    is_first_time = not r
    print(f"{is_first_time=}")

    are_any_rows_present = get_player_order_model() \
        .objects \
        .filter(level_id=level_id, user_id=user_id)\
        .exists()


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

                return {
                    "status": True
                }


            else:
                print("err 2 -----------------------------------")

        return {
            "status": False
        }
