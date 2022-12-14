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
        },
        "3": {
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
        }

    }


def _get_player_one_moves():
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
            "row": 1,
            "column": 8
          },
          "14": {
            "row": 2,
            "column": 8
          },
          "15": {
            "row": 3,
            "column": 8
          },
          "16": {
            "row": 4,
            "column": 8
          },
          "17": {
            "row": 5,
            "column": 8
          },
          "18": {
            "row": 6,
            "column": 9
          },
          "19": {
            "row": 6,
            "column": 10
          },
          "20": {
            "row": 6,
            "column": 11
          },
          "21": {
            "row": 6,
            "column": 12
          },
          "22": {
            "row": 6,
            "column": 13
          },
          "23": {
            "row": 6,
            "column": 14
          },
          "24": {
            "row": 7,
            "column": 14
          },
          "25": {
            "row": 8,
            "column": 14
          },
          "26": {
            "row": 8,
            "column": 13
          },
          "27": {
            "row": 8,
            "column": 12
          },
          "28": {
            "row": 8,
            "column": 11
          },
          "29": {
            "row": 8,
            "column": 10
          },
          "30": {
            "row": 8,
            "column": 9
          },
          "31": {
            "row": 9,
            "column": 8
          },
          "32": {
            "row": 10,
            "column": 8
          },
          "33": {
            "row": 11,
            "column": 8
          },
          "34": {
            "row": 12,
            "column": 8
          },
          "35": {
            "row": 13,
            "column": 8
          },
          "36": {
            "row": 14,
            "column": 8
          },
          "37": {
            "row": 14,
            "column": 7
          },
          "38": {
            "row": 14,
            "column": 6
          },
          "39": {
            "row": 13,
            "column": 6
          },
          "40": {
            "row": 12,
            "column": 6
          },
          "41": {
            "row": 11,
            "column": 6
          },
          "42": {
            "row": 10,
            "column": 6
          },
          "43": {
            "row": 9,
            "column": 6
          },
          "44": {
            "row": 8,
            "column": 5
          },
          "45": {
            "row": 8,
            "column": 4
          },
          "46": {
            "row": 8,
            "column": 3
          },
          "47": {
            "row": 8,
            "column": 2
          },
          "48": {
            "row": 8,
            "column": 1
          },
          "49": {
            "row": 8,
            "column": 0
          },
          "50": {
            "row": 7,
            "column": 0
          },
          "51": {
            "row": 7,
            "column": 1
          },
          "52": {
            "row": 7,
            "column": 2
          },
          "53": {
            "row": 7,
            "column": 3
          },
          "54": {
            "row": 7,
            "column": 4
          },
          "55": {
            "row": 7,
            "column": 5
          },
          "56": {
            "row": 7,
            "column": 6
          }
        }


def _get_player_two_moves():
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
    "column": 13
  },
  "14": {
    "row": 8,
    "column": 12
  },
  "15": {
    "row": 8,
    "column": 11
  },
  "16": {
    "row": 8,
    "column": 10
  },
  "17": {
    "row": 8,
    "column": 9
  },
  "18": {
    "row": 9,
    "column": 8
  },
  "19": {
    "row": 10,
    "column": 8
  },
  "20": {
    "row": 11,
    "column": 8
  },
  "21": {
    "row": 12,
    "column": 8
  },
  "22": {
    "row": 13,
    "column": 8
  },
  "23": {
    "row": 14,
    "column": 8
  },
  "24": {
    "row": 14,
    "column": 7
  },
  "25": {
    "row": 14,
    "column": 6
  },
  "26": {
    "row": 13,
    "column": 6
  },
  "27": {
    "row": 12,
    "column": 6
  },
  "28": {
    "row": 11,
    "column": 6
  },
  "29": {
    "row": 10,
    "column": 6
  },
  "30": {
    "row": 9,
    "column": 6
  },
  "31": {
    "row": 8,
    "column": 5
  },
  "32": {
    "row": 8,
    "column": 4
  },
  "33": {
    "row": 8,
    "column": 3
  },
  "34": {
    "row": 8,
    "column": 2
  },
  "35": {
    "row": 8,
    "column": 1
  },
  "36": {
    "row": 8,
    "column": 0
  },
  "37": {
    "row": 7,
    "column": 0
  },
  "38": {
    "row": 6,
    "column": 0
  },
  "39": {
    "row": 6,
    "column": 1
  },
  "40": {
    "row": 6,
    "column": 2
  },
  "41": {
    "row": 6,
    "column": 3
  },
  "42": {
    "row": 6,
    "column": 4
  },
  "43": {
    "row": 6,
    "column": 5
  },
  "44": {
    "row": 5,
    "column": 6
  },
  "45": {
    "row": 4,
    "column": 6
  },
  "46": {
    "row": 3,
    "column": 6
  },
  "47": {
    "row": 2,
    "column": 6
  },
  "48": {
    "row": 1,
    "column": 6
  },
  "49": {
    "row": 0,
    "column": 6
  },
  "50": {
    "row": 0,
    "column": 7
  },
  "51": {
    "row": 1,
    "column": 7
  },
  "52": {
    "row": 2,
    "column": 7
  },
  "53": {
    "row": 3,
    "column": 7
  },
  "54": {
    "row": 4,
    "column": 7
  },
  "55": {
    "row": 5,
    "column": 7
  },
  "56": {
    "row": 6,
    "column": 7
  }
}


def _get_player_three_moves():
    return {
          "0": {
            "row": 8,
            "column": 13
          },
          "1": {
            "row": 8,
            "column": 12
          },
          "2": {
            "row": 8,
            "column": 11
          },
          "3": {
            "row": 8,
            "column": 10
          },
          "4": {
            "row": 8,
            "column": 9
          },
          "5": {
            "row": 9,
            "column": 8
          },
          "6": {
            "row": 10,
            "column": 8
          },
          "7": {
            "row": 11,
            "column": 8
          },
          "8": {
            "row": 12,
            "column": 8
          },
          "9": {
            "row": 13,
            "column": 8
          },
          "10": {
            "row": 14,
            "column": 8
          },
          "11": {
            "row": 14,
            "column": 7
          },
          "12": {
            "row": 14,
            "column": 6
          },
          "13": {
            "row": 13,
            "column": 6
          },
          "14": {
            "row": 12,
            "column": 6
          },
          "15": {
            "row": 11,
            "column": 6
          },
          "16": {
            "row": 10,
            "column": 6
          },
          "17": {
            "row": 9,
            "column": 6
          },
          "18": {
            "row": 8,
            "column": 5
          },
          "19": {
            "row": 8,
            "column": 4
          },
          "20": {
            "row": 8,
            "column": 3
          },
          "21": {
            "row": 8,
            "column": 2
          },
          "22": {
            "row": 8,
            "column": 1
          },
          "23": {
            "row": 8,
            "column": 0
          },
          "24": {
            "row": 7,
            "column": 0
          },
          "25": {
            "row": 6,
            "column": 0
          },
          "26": {
            "row": 6,
            "column": 1
          },
          "27": {
            "row": 6,
            "column": 2
          },
          "28": {
            "row": 6,
            "column": 3
          },
          "29": {
            "row": 6,
            "column": 4
          },
          "30": {
            "row": 6,
            "column": 5
          },
          "31": {
            "row": 5,
            "column": 6
          },
          "32": {
            "row": 4,
            "column": 6
          },
          "33": {
            "row": 3,
            "column": 6
          },
          "34": {
            "row": 2,
            "column": 6
          },
          "35": {
            "row": 1,
            "column": 6
          },
          "36": {
            "row": 0,
            "column": 6
          },
          "37": {
            "row": 0,
            "column": 7
          },
          "38": {
            "row": 0,
            "column": 8
          },
          "39": {
            "row": 1,
            "column": 8
          },
          "40": {
            "row": 2,
            "column": 8
          },
          "41": {
            "row": 3,
            "column": 8
          },
          "42": {
            "row": 4,
            "column": 8
          },
          "43": {
            "row": 5,
            "column": 8
          },
          "44": {
            "row": 6,
            "column": 9
          },
          "45": {
            "row": 6,
            "column": 10
          },
          "46": {
            "row": 6,
            "column": 11
          },
          "47": {
            "row": 6,
            "column": 12
          },
          "48": {
            "row": 6,
            "column": 13
          },
          "49": {
            "row": 6,
            "column": 14
          },
          "50": {
            "row": 7,
            "column": 14
          },
          "51": {
            "row": 7,
            "column": 13
          },
          "52": {
            "row": 7,
            "column": 12
          },
          "53": {
            "row": 7,
            "column": 11
          },
          "54": {
            "row": 7,
            "column": 10
          },
          "55": {
            "row": 7,
            "column": 9
          },
          "56": {
            "row": 7,
            "column": 8
          }
        }


def _get_player_four_moves():
    return {
  "0": {
    "row": 13,
    "column": 6
  },
  "1": {
    "row": 12,
    "column": 6
  },
  "2": {
    "row": 11,
    "column": 6
  },
  "3": {
    "row": 10,
    "column": 6
  },
  "4": {
    "row": 9,
    "column": 6
  },
  "5": {
    "row": 8,
    "column": 5
  },
  "6": {
    "row": 8,
    "column": 4
  },
  "7": {
    "row": 8,
    "column": 3
  },
  "8": {
    "row": 8,
    "column": 2
  },
  "9": {
    "row": 8,
    "column": 1
  },
  "10": {
    "row": 8,
    "column": 0
  },
  "11": {
    "row": 7,
    "column": 0
  },
  "12": {
    "row": 6,
    "column": 0
  },
  "13": {
    "row": 6,
    "column": 1
  },
  "14": {
    "row": 6,
    "column": 2
  },
  "15": {
    "row": 6,
    "column": 3
  },
  "16": {
    "row": 6,
    "column": 4
  },
  "17": {
    "row": 6,
    "column": 5
  },
  "18": {
    "row": 5,
    "column": 6
  },
  "19": {
    "row": 4,
    "column": 6
  },
  "20": {
    "row": 3,
    "column": 6
  },
  "21": {
    "row": 2,
    "column": 6
  },
  "22": {
    "row": 1,
    "column": 6
  },
  "23": {
    "row": 0,
    "column": 6
  },
  "24": {
    "row": 0,
    "column": 7
  },
  "25": {
    "row": 0,
    "column": 8
  },
  "26": {
    "row": 1,
    "column": 8
  },
  "27": {
    "row": 2,
    "column": 8
  },
  "28": {
    "row": 3,
    "column": 8
  },
  "29": {
    "row": 4,
    "column": 8
  },
  "30": {
    "row": 5,
    "column": 8
  },
  "31": {
    "row": 6,
    "column": 9
  },
  "32": {
    "row": 6,
    "column": 10
  },
  "33": {
    "row": 6,
    "column": 11
  },
  "34": {
    "row": 6,
    "column": 12
  },
  "35": {
    "row": 6,
    "column": 13
  },
  "36": {
    "row": 6,
    "column": 14
  },
  "37": {
    "row": 7,
    "column": 14
  },
  "38": {
    "row": 8,
    "column": 14
  },
  "39": {
    "row": 8,
    "column": 13
  },
  "40": {
    "row": 8,
    "column": 12
  },
  "41": {
    "row": 8,
    "column": 11
  },
  "42": {
    "row": 8,
    "column": 10
  },
  "43": {
    "row": 8,
    "column": 9
  },
  "44": {
    "row": 9,
    "column": 8
  },
  "45": {
    "row": 10,
    "column": 8
  },
  "46": {
    "row": 11,
    "column": 8
  },
  "47": {
    "row": 12,
    "column": 8
  },
  "48": {
    "row": 13,
    "column": 8
  },
  "49": {
    "row": 14,
    "column": 8
  },
  "50": {
    "row": 14,
    "column": 7
  },
  "51": {
    "row": 13,
    "column": 7
  },
  "52": {
    "row": 12,
    "column": 7
  },
  "53": {
    "row": 11,
    "column": 7
  },
  "54": {
    "row": 10,
    "column": 7
  },
  "55": {
    "row": 9,
    "column": 7
  },
  "56": {
    "row": 8,
    "column": 7
  }
}


def get_moves():
    return {
        0: _get_player_one_moves(),
        1: _get_player_two_moves(),
        2: _get_player_three_moves(),
        3: _get_player_four_moves()
    }


def get_players():
    return {
        '0': {
            'colour': 'green',
            'username': '0 username / nickname',

        },
        '1': {
            'colour': 'blue',
            'username': '1 username / nickname',

        },
        '2': {
            'colour': 'yellow',
            'username': '2 username / nickname',

        },
        '3': {
            'colour': 'red',
            'username': '3 username / nickname',
        }
    }


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

def getMap():
    return [
        [' ', ' ', ' ', ' ', ' ', ' ', 'b', 'b', 'b', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '1', '-', '-', '2', ' ', 'b', 'b', 'b', ' ', '1', '-', '-', '2', ' '],
        [' ', '|', 'q', 'q', '|', ' ', 'b', 'b', 'b', ' ', '|', 'w', 'w', '|', ' '],
        [' ', '|', 'q', 'q', '|', ' ', 'b', 'b', 'b', ' ', '|', 'w', 'w', '|', ' '],
        [' ', '4', '-', '-', '3', ' ', 'b', 'b', 'b', ' ', '4', '-', '-', '3', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', 'b', 'b', 'b', ' ', ' ', ' ', ' ', ' ', ' '],
        ['b', 'b', 'b', 'b', 'b', 'b', ' ', ' ', ' ', 'b', 'b', 'b', 'b', 'b', 'b'],
        ['b', 'b', 'b', 'b', 'b', 'b', ' ', ' ', ' ', 'b', 'b', 'b', 'b', 'b', 'b'],
        ['b', 'b', 'b', 'b', 'b', 'b', ' ', ' ', ' ', 'b', 'b', 'b', 'b', 'b', 'b'],
        [' ', ' ', ' ', ' ', ' ', ' ', 'b', 'b', 'b', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '1', '-', '-', '2', ' ', 'b', 'b', 'b', ' ', '1', '-', '-', '2', ' '],
        [' ', '|', 'e', 'e', '|', ' ', 'b', 'b', 'b', ' ', '|', 'r', 'r', '|', ' '],
        [' ', '|', 'e', 'e', '|', ' ', 'b', 'b', 'b', ' ', '|', 'r', 'r', '|', ' '],
        [' ', '4', '-', '-', '3', ' ', 'b', 'b', 'b', ' ', '4', '-', '-', '3', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', 'b', 'b', 'b', ' ', ' ', ' ', ' ', ' ', ' '],
    ]
