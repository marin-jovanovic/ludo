from collections import defaultdict

from backend.api.model.acceptance_log import get_acceptance_log_model
from backend.api.model.level_log import get_level_log_model


def clean(level_id):
    print("clean")

    """
    all { "status": true, "entryIndex": 141, "id": 3325 }
    any { "status": true, "entryIndex": 141, "id": 3325 }
    this{ "status": true, "entryIndex": 141, "id": 3325 } 

    index	entryId	userJoinIndex	action	diceResult	tokenId	performed
    141	    3326	1	            move	3	        0	    false

    """

    # capacity = get_level_model().objects.get(id=level_id).capacity
    #
    # fix_1(capacity, level_id)
    #
    # fix_2(level_id)
    #
    # fix_3(level_id)
    #
    # # fix_4(level_id)
    #
    # fix_5(level_id)


def fix_5(level_id):
    """
    delete all wrongly generated
    """

    log = get_level_log_model() \
        .objects \
        .filter(game_id=level_id) \
        .values("id",
                "action",
                "performed").order_by(
        "-id")

    log = list(log)
    first_id = log[0]["id"]
    choose_count = 0
    last = None
    for i in log:
        if i["performed"]:
            break

        last = i

        if i["action"] == "choose":
            choose_count += 1

        print(i)
    print(f"{last=}")
    if choose_count != 0 and choose_count != 1:
        if last["action"] == "choose":
            print("del")

            for i in range(last["id"] + 1, first_id + 1):
                print("staging for deleting", i)
                get_level_log_model().objects.filter(id=i).delete()


# def fix_4(level_id):
#
#     """if last log is choose and true and we have log for that
#     just generate new
#     """
#
#     log = get_level_log_model().objects.filter(
#         game_id=level_id).values().order_by("id")
#     log = list(log)
#
#     last_entry = log[-1]
#
#     if last_entry["action"] == "choose":
#         last_entry_id = last_entry["id"]
#
#         l = get_level_log_model().objects.get(
#             id=last_entry_id)
#
#         l.performed = False
#         l.save()
#
#         get_acceptance_log_model().objects.filter(
#             log_entry_id=last_entry_id
#         ).delete()
#
#     """now try generating new rows"""
#
#     r = try_generating_api(log, level_id)
#
#     print(f"{r=}")
#
#     if not r["logDiff"]:
#         return
#
#     log_diff = r["logDiff"]
#     log = r["log"]
#
#     t = join_id_to_username_and_user_id(r["turn"], level_id)
#     if not t["status"]:
#         print("err join_id_to_username_and_user_id")
#
#     # add to db log diff
#
#     r = level_id_to_name(level_id)
#     if not r["status"]:
#         print("err level_id_to_name")
#         sys.exit(-1)
#         return r
#
#
#     level_name = r["payload"]
#
#     log = get_level_log_model().objects.filter(
#         game_id=level_id).values().order_by("id")
#     log = list(log)
#     last_entry = log[-1]
#
#     is_last_entry_choose = last_entry["action"] == "choose"
#
#     for i in log_diff[:-1]:
#
#         i["game"] = level_name
#         print("adding", i)
#         add_entry(**i)
#
#     if not is_last_entry_choose:
#         i = log_diff[-1]
#
#         i["game"] = level_name
#         print("adding", i)
#         add_entry(**i)

def fix_3(level_id):
    """go over acceptance log and find everything that is
    confirmed but does not exist in level lgo"""

    acceptance_log = get_acceptance_log_model().objects.filter(
        level_id=level_id)

    log = get_level_log_model().objects \
        .filter(game_id=level_id) \
        .values("id")

    log = list(log)

    log = [i["id"] for i in log]

    # print(f"{log=}")

    to_del = []
    for i in acceptance_log:
        if i.log_entry_id not in log:
            print("delete", i.log_entry_id, i.id)
            to_del.append(i.id)

    if not to_del:
        # print("nothing to del")
        return

    for i in to_del:
        print("del", i, type(i))
        get_acceptance_log_model().objects.get(id=i).delete()

        # if not i.log_entry_id:
        #     print("")


def fix_2(level_id):
    """
        log
        141
        141
        142
        142
        143
        144

        duplicates are present

        why this happened?
        someone sent post?

    """

    log = get_level_log_model().objects \
        .filter(game_id=level_id) \
        .values("instruction_id").order_by("instruction_id")

    r = defaultdict(int)

    for i in log:
        r[i["instruction_id"]] += 1

    to_remove = []

    for id_, c in r.items():
        if c != 1:
            to_remove.append(id_)

    if not to_remove:
        return

    smallest_duplicate = min(to_remove)

    print("fix remove everything from (including)", smallest_duplicate)

    everything_after_including_smallest = get_level_log_model().objects \
        .filter(game_id=level_id,
                instruction_id__gte=smallest_duplicate).values()

    everything_after_including_smallest = list(
        everything_after_including_smallest)

    for i in everything_after_including_smallest:
        print("fix staging: deleting", i)

    get_level_log_model().objects.filter(game_id=level_id,
                                         instruction_id__gte=smallest_duplicate).delete()

    # todo now clear acceptance log


def fix_1(capacity, level_id):
    """
    if not performed in level_log but count in acceptance_log is >= capacity
        then set performed to true


    """
    log = get_level_log_model().objects.filter(game_id=level_id,
                                               performed=False).values(
        "instruction_id", "id").order_by("instruction_id").distinct()
    for i in log:
        log_entry_id = i["id"]

        r = get_acceptance_log_model().objects \
            .filter(level_id=level_id, log_entry_id=log_entry_id) \
            .values("user_id").distinct().count()

        if r >= capacity:
            print("todo [fix] this by confirming")
