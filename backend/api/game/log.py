def construct_goes(player):
    """
    for determine_order
    """

    return {
        "game": None,
        "player": player,
        "token": None,
        "dice_result": None,
        "action": "goes"
    }


def construct_roll(player, roll):
    """
    @player rolled @roll

    """
    return {
        "game": None,
        "player": player,
        "token": None,
        "dice_result": roll,
        "action": "roll"
    }


def construct_tie():
    """
    for determine_order
    """
    return {
        "game": None,
        "player": None,
        "token": None,
        "dice_result": None,
        "action": "tie"
    }

def choose(player):
    return {
        "game": None,
        "player": player,
        "token": None,
        "dice_result": None,
        "action": "choose"
    }

def skip(player):
    """
    player skip its turn; no action

    """

    return {
        "game": None,
        "player": player,
        "token": None,
        "dice_result": None,
        "action": "skip"
    }


def move_token( player, token, step):
    return {
        'game': None,
        'player': player,
        'token': token,
        'dice_result': step,
        'action': "move"
    }
