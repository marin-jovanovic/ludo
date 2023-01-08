from backend.api.game.log import user_choose


def artificially_add_choose_row(log: list) -> list:
    """
    Add a choose row to the log based on the last entry in the log.

    Parameters:
    log (list): A list of dictionaries representing the log.

    Returns:
    list: The modified log with the choose row added.

    """

    last_entry = log[-1]

    if last_entry["action"] == "roll":
        new_entry = user_choose(player=last_entry["player"], roll=last_entry["dice_result"])
        log.append(new_entry)
    if last_entry["action"] == "won":
        pass
    else:
        print("err artificially_add_choose_row", last_entry)
    return log


# remove last choose when loading ? or remove all
def artificially_remove_choose_entries(log: list) -> list:
    """
    Remove choose entries from the log.

    Parameters:
    log (list): A list of dictionaries representing the log.

    Returns:
    list: The modified log with the choose entries removed.

    """
    new_log = []
    for entry in log:
        if entry["action"] == "choose":
            print(f"{entry=}")
        else:
            new_log.append(entry)

    return new_log
