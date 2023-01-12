from backend.api.game.game import Level, choose
# from backend.api.game.adapter import artificially_add_choose_row
from backend.api.game.log import user_choose


def create_level(level_id):

    """order is guaranteed of entries in log"""

    level = Level(level_id=level_id)

    # log = artificially_add_choose_row(level.get_log())

    log = level.get_log()

    return {
        "status": True,
        "payload": log
    }

def try_generating_api(log, level_id):
    # log = artificially_remove_choose_entries(log)

    in_len_log = len(log)

    # preprocess if loaded from db
    for i in log:
        for j in ["id", "game_id", "instruction_id", "performed"]:
            if j in i:
                del i[j]

    # todo eating, game won, game lost, ...

    level = Level(log=log, level_id=level_id)

    log_diff = log[in_len_log:]

    to_choose = {**level.start_pool_options, **level.non_start_pool_options}

    last_entry = level.get_log()[-1]
    if last_entry["action"] != "roll":
        print("errr last log entry is not roll, i think game is done")
        return


    # todo this needs to be renamed to user join index
    player = last_entry['player']

    # if log_diff :
    #
    #     log_diff = artificially_add_choose_row(log_diff)

    if not log_diff:
        print("err? nothing generated")

        if last_entry["action"] == "roll":
            new_entry = user_choose(player=last_entry["player"], roll=last_entry["dice_result"])
            log_diff.append(new_entry)

    return {
        "log": level.get_log_as_dict(),
        "logDiff": log_diff,
        "turn": player,
        "legalMoves": list(to_choose.keys())
    }


def add_entry_to_log(log, player_id, token_id, level_id):
    """
    player_id wants to move token_id

    check if they can do that (if that move is legal)

    does not handle security part


    """
    # preprocess if loaded from db
    # log = artificially_remove_choose_entries(log)
    player_id = int(player_id)
    token_id = int(token_id)
    for i in log:
        for j in ["id", "game_id", "instruction_id", "performed"]:
            if j in i:
                del i[j]

    in_len_log = len(log)

    # todo eating, game won, game lost, ...

    level = Level(log=log, level_id=level_id)

    # update level objects
    choose(
        board=level.board,
        log=level.get_log(),
        player_id=player_id,
        token_id=token_id
    )

    # perfrom as much as you can new instructions
    level = Level(log=level.get_log(), level_id=level_id)


    log_diff = level.get_log()[in_len_log:]

    log_diff_as_dict = {}
    for index, entry in level.get_log_as_dict().items():
        # art todo add
        if index < in_len_log:
            continue

        log_diff_as_dict[index] = entry

    c = 0
    for index,entry in log_diff_as_dict.items():
        if not entry == log_diff[c]:
            print(f"err mismatch {log_diff_as_dict=} {log_diff=}")
        c += 1

    to_choose = {**level.start_pool_options, **level.non_start_pool_options}

    last_log = level.get_log()[-1]
    # fixme can be choose in new impl
    # if last_log["action"] != "roll":
    #     print("errr last log entry is not roll")
    #     return

    # todo this needs to be renamed to user
    player = last_log['player']

    return {
        "logDiffAsDict": log_diff_as_dict,
        # "log": entire_log_as_dict,
        # "logDiff": log_diff,
        "turn": player,
        "legalMoves": list(to_choose.keys())
    }



def get_log_api(log, level_id):
    """"""
    # todo i think this exists somewhere else and logic is ok

    # log = artificially_remove_choose_entries(log)

    # preprocess if loaded from db
    for entry in log:
        for attribute in ["id", "game_id", "instruction_id", "performed"]:
            if attribute in entry:
                del entry[attribute]

    level = Level(log=log, level_id=level_id)

    to_choose = {**level.start_pool_options, **level.non_start_pool_options}

    last_log = level.get_log()[-1]
    # todo roll -> roll + choose
    # if last_log["action"] != "roll":
    #     print("errr last log entry is not roll")
    #     return {"turn": None, "legalMoves": []}

    # todo this needs to be renamed to user
    player = last_log['player']

    return {
        "turn": player,
        "legalMoves": list(to_choose.keys())
    }




#     # todo what if user quits mid game, -> need to split log
#     #   generate without them


# def main():
#     from backend.api.cqrs_q.level import level_name_to_level_id
#     r = level_name_to_level_id(level_name)
#     if not r["status"]:
#         return r
#     level_name = r["payload"]
#
#     t = create_game_api(level_name)
#
#     if not t["status"]:
#         print("not status")
#
#     log = t["payload"]
#     for e, i in enumerate(log):
#         print(e, i)
#
#     print(80 * "-")
#
#     last_entry =  log[-1]
#
#     r = add_entry_to_log(log, last_entry["player"], 0)
#
#     log_diff = r["logDiff"]
#     turn = r["turn"]
#     legal_moves = r["legalMoves"]
#
#     log = log + log_diff
#     last_entry = log[-1]
#
#     print()
#     print("log diff")
#     for e, i in enumerate(log_diff):
#         print(e, i)
#
#     print()
#     print("log")
#     for e, i in enumerate(log):
#         print(e, i)
#
#     print(80 * "-")
#
#     r = add_entry_to_log(log, last_entry["player"], legal_moves[0])
#
#     log_diff = r["logDiff"]
#     turn = r["turn"]
#     legal_moves = r["legalMoves"]
#
#     print()
#     print("log diff")
#     for e, i in enumerate(log_diff):
#         print(e, i)
#
#     print()
#     print("log")
#     for e, i in enumerate(log):
#         print(e, i)
#
#     # for i in r:
#     #     print(i)
#     #
#     # print(r)
#     #
#     # log = r["payload"]
#     #
#     #
#     #
#     # print()
#     # for e, i in enumerate(log):
#     #     print(e, i)
#     # print()
#
#
#     return
#     t = get_log_api(log)
#
#     print(f"{t=}")
#
#     return
#
#     r = add_entry_to_log(log, last["player"], 0)
#
#
#     log = t["payload"]
#     last = t["payload"][-1]
#
#     for e, i in enumerate(log):
#         print(e, i)
#     print()
#
#     print(f"{last=}")
#
#
#     print("r")
#     for k,v in r.items():
#         print(k,v)
#
#     print("log diff")
#     for e, i in enumerate(r["logDiff"]):
#         print(e, i)
#
#     print()
#     print()
#     print()
#     print()
#
#     log = log + r["logDiff"]
#     last = t["payload"][-1]
#
#     r = add_entry_to_log(log, last["player"], 0)
#     print("r")
#     for k,v in r.items():
#         print(k,v)
#
#     print("log diff")
#     for e, i in enumerate(r["logDiff"]):
#         print(e, i)
#
# if __name__ == '__main__':
#     main()
