def get_config():
    return {
        "number of players": 2,
        "tokens per player": 4,
        "dice number of sides": 6,

        # assumption: talking for each player individually
        # if True: all tokens must reach the same destination
        # else: each token has it unique(multiple can go to same destination, but it is not a rule)
        # destination location
        "flag: same destination": True,

        # highest: highest goes first and then clockwise or anticlockwise (6, right, right, right)
        # order: 1st, 2nd, 3rd, 4th highest roll (6, 3, 2, 1)
        'choice: highest; order': True,

        # if highest then in which direction
        'choice: clockwise; anticlockwise': False,

        # when rolling dice to see who goes first
        # skip if tie will occur
        'flag: tie in order': False,

    }
