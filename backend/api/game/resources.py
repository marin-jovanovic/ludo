def get_start_pool():
    """

    player_id: {
        token_id: {
            "row": row,
            "column": column
        }
    }

    """

    return {
        "0": {
            "0": {
                "row": 2,
                "column": 2
            },
            "1": {
                "row": 2,
                "column": 3
            },
            "2": {
                "row": 3,
                "column": 2
            },
            "3": {
                "row": 3,
                "column": 3
            }

        },
        "1": {

            "0": {
                "row": 2,
                "column": 11
            },
            "1": {
                "row": 3,
                "column": 11
            },
            "2": {
                "row": 2,
                "column": 12
            },
            "3": {
                "row": 3,
                "column": 12
            }

        },
        "2": {
            "0": {
                "row": 11,
                "column": 2
            },
            "1": {
                "row": 12,
                "column": 2
            },
            "2": {
                "row": 11,
                "column": 3
            },
            "3": {
                "row": 12,
                "column": 3
            }
        },
        "3": {
            "0": {
                "row": 11,
                "column": 11
            },
            "1": {
                "row": 12,
                "column": 11
            },
            "2": {
                "row": 11,
                "column": 12
            },
            "3": {
                "row": 12,
                "column": 12
            }
        }

    }


def get_player_one_moves():
    """
        tile_id is relative to this player

        tile_id: {
            "row": row,
            "column": column
        }
    """

    return {
        "0": {
            "row": 6,
            "column": 1
        },
        "1": {
            "row": 6,
            "column": 2
        },
        "2": {
            "row": 6,
            "column": 3
        },
        "3": {
            "row": 6,
            "column": 4
        },
        "4": {
            "row": 6,
            "column": 5
        },
        "5": {
            "row": 5,
            "column": 6
        },
        "6": {
            "row": 4,
            "column": 6
        },
        "7": {
            "row": 3,
            "column": 6
        },
        "8": {
            "row": 2,
            "column": 6
        },
        "9": {
            "row": 1,
            "column": 6
        },
        "10": {
            "row": 0,
            "column": 6
        },
        "11": {
            "row": 0,
            "column": 7
        },
        "12": {
            "row": 0,
            "column": 8
        },
        "13": {
            "row": 2,
            "column": 8
        },
        "14": {
            "row": 3,
            "column": 8
        },
        "15": {
            "row": 4,
            "column": 8
        },
        "16": {
            "row": 5,
            "column": 8
        },
        "17": {
            "row": 6,
            "column": 9
        },
        "18": {
            "row": 6,
            "column": 10
        },
        "19": {
            "row": 6,
            "column": 11
        },
        "20": {
            "row": 6,
            "column": 12
        },
        "21": {
            "row": 6,
            "column": 13
        },
        "22": {
            "row": 6,
            "column": 14
        },
        "23": {
            "row": 7,
            "column": 14
        },
        "24": {
            "row": 8,
            "column": 14
        },
        "25": {
            "row": 8,
            "column": 12
        },
        "26": {
            "row": 8,
            "column": 11
        },
        "27": {
            "row": 8,
            "column": 10
        },
        "28": {
            "row": 8,
            "column": 9
        },
        "29": {
            "row": 9,
            "column": 8
        },
        "30": {
            "row": 10,
            "column": 8
        },
        "31": {
            "row": 11,
            "column": 8
        },
        "32": {
            "row": 12,
            "column": 8
        },
        "33": {
            "row": 13,
            "column": 8
        },
        "34": {
            "row": 14,
            "column": 8
        },
        "35": {
            "row": 14,
            "column": 7
        },
        "36": {
            "row": 14,
            "column": 6
        },
        "37": {
            "row": 12,
            "column": 6
        },
        "38": {
            "row": 11,
            "column": 6
        },
        "39": {
            "row": 10,
            "column": 6
        },
        "40": {
            "row": 9,
            "column": 6
        },
        "41": {
            "row": 8,
            "column": 5
        },
        "42": {
            "row": 8,
            "column": 4
        },
        "43": {
            "row": 8,
            "column": 3
        },
        "44": {
            "row": 8,
            "column": 2
        },
        "45": {
            "row": 8,
            "column": 1
        },
        "46": {
            "row": 8,
            "column": 0
        },
        "47": {
            "row": 7,
            "column": 0
        },
        "48": {
            "row": 7,
            "column": 1
        },
        "49": {
            "row": 7,
            "column": 2
        },
        "50": {
            "row": 7,
            "column": 3
        },
        "51": {
            "row": 7,
            "column": 4
        },
        "52": {
            "row": 7,
            "column": 5
        },
        "53": {
            "row": 7,
            "column": 6
        }
    }


def get_player_two_moves():
    return {
        "0": {
            "row": 1,
            "column": 8
        },
        "1": {
            "row": 2,
            "column": 8
        },
        "2": {
            "row": 3,
            "column": 8
        },
        "3": {
            "row": 4,
            "column": 8
        },
        "4": {
            "row": 5,
            "column": 8
        },
        "5": {
            "row": 6,
            "column": 9
        },
        "6": {
            "row": 6,
            "column": 10
        },
        "7": {
            "row": 6,
            "column": 11
        },
        "8": {
            "row": 6,
            "column": 12
        },
        "9": {
            "row": 6,
            "column": 13
        },
        "10": {
            "row": 6,
            "column": 14
        },
        "11": {
            "row": 7,
            "column": 14
        },
        "12": {
            "row": 8,
            "column": 14
        },
        "13": {
            "row": 8,
            "column": 12
        },
        "14": {
            "row": 8,
            "column": 11
        },
        "15": {
            "row": 8,
            "column": 10
        },
        "16": {
            "row": 8,
            "column": 9
        },
        "17": {
            "row": 9,
            "column": 8
        },
        "18": {
            "row": 10,
            "column": 8
        },
        "19": {
            "row": 11,
            "column": 8
        },
        "20": {
            "row": 12,
            "column": 8
        },
        "21": {
            "row": 13,
            "column": 8
        },
        "22": {
            "row": 14,
            "column": 8
        },
        "23": {
            "row": 14,
            "column": 7
        },
        "24": {
            "row": 14,
            "column": 6
        },
        "25": {
            "row": 12,
            "column": 6
        },
        "26": {
            "row": 11,
            "column": 6
        },
        "27": {
            "row": 10,
            "column": 6
        },
        "28": {
            "row": 9,
            "column": 6
        },
        "29": {
            "row": 8,
            "column": 5
        },
        "30": {
            "row": 8,
            "column": 4
        },
        "31": {
            "row": 8,
            "column": 3
        },
        "32": {
            "row": 8,
            "column": 2
        },
        "33": {
            "row": 8,
            "column": 1
        },
        "34": {
            "row": 8,
            "column": 0
        },
        "35": {
            "row": 7,
            "column": 0
        },
        "36": {
            "row": 6,
            "column": 0
        },
        "37": {
            "row": 6,
            "column": 2
        },
        "38": {
            "row": 6,
            "column": 3
        },
        "39": {
            "row": 6,
            "column": 4
        },
        "40": {
            "row": 6,
            "column": 5
        },
        "41": {
            "row": 5,
            "column": 6
        },
        "42": {
            "row": 4,
            "column": 6
        },
        "43": {
            "row": 3,
            "column": 6
        },
        "44": {
            "row": 2,
            "column": 6
        },
        "45": {
            "row": 1,
            "column": 6
        },
        "46": {
            "row": 0,
            "column": 6
        },
        "47": {
            "row": 0,
            "column": 7
        },
        "48": {
            "row": 1,
            "column": 7
        },
        "49": {
            "row": 2,
            "column": 7
        },
        "50": {
            "row": 3,
            "column": 7
        },
        "51": {
            "row": 4,
            "column": 7
        },
        "52": {
            "row": 5,
            "column": 7
        },
        "53": {
            "row": 6,
            "column": 7
        }
    }


def get_config():
    return {
        "number of players": 4,
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
