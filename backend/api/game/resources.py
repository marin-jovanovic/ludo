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
            "row": "2",
            "column": "2",
            "type": "1"
        },
        "1": {
            "row": "3",
            "column": "2",
            "type": "1"
        },
        "2": {
            "row": "2",
            "column": "3",
            "type": "1"
        },
        "3": {
            "row": "3",
            "column": "3",
            "type": "1"
        },
        "4": {
            "row": "6",
            "column": "1",
            "type": "2"
        },
        "5": {
            "row": "6",
            "column": "2",
            "type": "2"
        },
        "6": {
            "row": "6",
            "column": "3",
            "type": "2"
        },
        "7": {
            "row": "6",
            "column": "4",
            "type": "2"
        },
        "8": {
            "row": "6",
            "column": "5",
            "type": "2"
        },
        "9": {
            "row": "5",
            "column": "6",
            "type": "2"
        },
        "10": {
            "row": "4",
            "column": "6",
            "type": "2"
        },
        "11": {
            "row": "3",
            "column": "6",
            "type": "2"
        },
        "12": {
            "row": "2",
            "column": "6",
            "type": "2"
        },
        "13": {
            "row": "1",
            "column": "6",
            "type": "2"
        },
        "14": {
            "row": "0",
            "column": "6",
            "type": "2"
        },
        "15": {
            "row": "0",
            "column": "7",
            "type": "2"
        },
        "16": {
            "row": "0",
            "column": "8",
            "type": "2"
        },
        "17": {
            "row": "1",
            "column": "8",
            "type": "2"
        },
        "18": {
            "row": "2",
            "column": "8",
            "type": "2"
        },
        "19": {
            "row": "3",
            "column": "8",
            "type": "2"
        },
        "20": {
            "row": "4",
            "column": "8",
            "type": "2"
        },
        "21": {
            "row": "5",
            "column": "8",
            "type": "2"
        },
        "22": {
            "row": "6",
            "column": "9",
            "type": "2"
        },
        "23": {
            "row": "6",
            "column": "10",
            "type": "2"
        },
        "24": {
            "row": "6",
            "column": "11",
            "type": "2"
        },
        "25": {
            "row": "6",
            "column": "12",
            "type": "2"
        },
        "26": {
            "row": "6",
            "column": "13",
            "type": "2"
        },
        "27": {
            "row": "6",
            "column": "14",
            "type": "2"
        },
        "28": {
            "row": "7",
            "column": "14",
            "type": "2"
        },
        "29": {
            "row": "8",
            "column": "14",
            "type": "2"
        },
        "30": {
            "row": "8",
            "column": "13",
            "type": "2"
        },
        "31": {
            "row": "8",
            "column": "12",
            "type": "2"
        },
        "32": {
            "row": "8",
            "column": "11",
            "type": "2"
        },
        "33": {
            "row": "8",
            "column": "10",
            "type": "2"
        },
        "34": {
            "row": "8",
            "column": "9",
            "type": "2"
        },
        "35": {
            "row": "9",
            "column": "8",
            "type": "2"
        },
        "36": {
            "row": "10",
            "column": "8",
            "type": "2"
        },
        "37": {
            "row": "11",
            "column": "8",
            "type": "2"
        },
        "38": {
            "row": "12",
            "column": "8",
            "type": "2"
        },
        "39": {
            "row": "13",
            "column": "8",
            "type": "2"
        },
        "40": {
            "row": "14",
            "column": "8",
            "type": "2"
        },
        "41": {
            "row": "14",
            "column": "7",
            "type": "2"
        },
        "42": {
            "row": "14",
            "column": "6",
            "type": "2"
        },
        "43": {
            "row": "13",
            "column": "6",
            "type": "2"
        },
        "44": {
            "row": "12",
            "column": "6",
            "type": "2"
        },
        "45": {
            "row": "11",
            "column": "6",
            "type": "2"
        },
        "46": {
            "row": "10",
            "column": "6",
            "type": "2"
        },
        "47": {
            "row": "9",
            "column": "6",
            "type": "2"
        },
        "48": {
            "row": "8",
            "column": "5",
            "type": "2"
        },
        "49": {
            "row": "8",
            "column": "4",
            "type": "2"
        },
        "50": {
            "row": "8",
            "column": "3",
            "type": "2"
        },
        "51": {
            "row": "8",
            "column": "2",
            "type": "2"
        },
        "52": {
            "row": "8",
            "column": "1",
            "type": "2"
        },
        "53": {
            "row": "8",
            "column": "0",
            "type": "2"
        },
        "54": {
            "row": "7",
            "column": "0",
            "type": "2"
        },
        "55": {
            "row": "7",
            "column": "1",
            "type": "3"
        },
        "56": {
            "row": "7",
            "column": "2",
            "type": "3"
        },
        "57": {
            "row": "7",
            "column": "3",
            "type": "3"
        },
        "58": {
            "row": "7",
            "column": "4",
            "type": "3"
        },
        "59": {
            "row": "7",
            "column": "5",
            "type": "3"
        },
        "60": {
            "row": "7",
            "column": "6",
            "type": "3"
        }
    }



def _get_player_two_moves():
    return {
        "0": {
            "row": "2",
            "column": "11",
            "type": "1"
        },
        "1": {
            "row": "3",
            "column": "11",
            "type": "1"
        },
        "2": {
            "row": "2",
            "column": "12",
            "type": "1"
        },
        "3": {
            "row": "3",
            "column": "12",
            "type": "1"
        },
        "4": {
            "row": "1",
            "column": "8",
            "type": "2"
        },
        "5": {
            "row": "2",
            "column": "8",
            "type": "2"
        },
        "6": {
            "row": "3",
            "column": "8",
            "type": "2"
        },
        "7": {
            "row": "4",
            "column": "8",
            "type": "2"
        },
        "8": {
            "row": "5",
            "column": "8",
            "type": "2"
        },
        "9": {
            "row": "6",
            "column": "9",
            "type": "2"
        },
        "10": {
            "row": "6",
            "column": "10",
            "type": "2"
        },
        "11": {
            "row": "6",
            "column": "11",
            "type": "2"
        },
        "12": {
            "row": "6",
            "column": "12",
            "type": "2"
        },
        "13": {
            "row": "6",
            "column": "13",
            "type": "2"
        },
        "14": {
            "row": "6",
            "column": "14",
            "type": "2"
        },
        "15": {
            "row": "7",
            "column": "14",
            "type": "2"
        },
        "16": {
            "row": "8",
            "column": "14",
            "type": "2"
        },
        "17": {
            "row": "8",
            "column": "13",
            "type": "2"
        },
        "18": {
            "row": "8",
            "column": "12",
            "type": "2"
        },
        "19": {
            "row": "8",
            "column": "11",
            "type": "2"
        },
        "20": {
            "row": "8",
            "column": "10",
            "type": "2"
        },
        "21": {
            "row": "8",
            "column": "9",
            "type": "2"
        },
        "22": {
            "row": "9",
            "column": "8",
            "type": "2"
        },
        "23": {
            "row": "10",
            "column": "8",
            "type": "2"
        },
        "24": {
            "row": "11",
            "column": "8",
            "type": "2"
        },
        "25": {
            "row": "12",
            "column": "8",
            "type": "2"
        },
        "26": {
            "row": "13",
            "column": "8",
            "type": "2"
        },
        "27": {
            "row": "14",
            "column": "8",
            "type": "2"
        },
        "28": {
            "row": "14",
            "column": "7",
            "type": "2"
        },
        "29": {
            "row": "14",
            "column": "6",
            "type": "2"
        },
        "30": {
            "row": "13",
            "column": "6",
            "type": "2"
        },
        "31": {
            "row": "12",
            "column": "6",
            "type": "2"
        },
        "32": {
            "row": "11",
            "column": "6",
            "type": "2"
        },
        "33": {
            "row": "10",
            "column": "6",
            "type": "2"
        },
        "34": {
            "row": "9",
            "column": "6",
            "type": "2"
        },
        "35": {
            "row": "8",
            "column": "5",
            "type": "2"
        },
        "36": {
            "row": "8",
            "column": "4",
            "type": "2"
        },
        "37": {
            "row": "8",
            "column": "3",
            "type": "2"
        },
        "38": {
            "row": "8",
            "column": "2",
            "type": "2"
        },
        "39": {
            "row": "8",
            "column": "1",
            "type": "2"
        },
        "40": {
            "row": "8",
            "column": "0",
            "type": "2"
        },
        "41": {
            "row": "7",
            "column": "0",
            "type": "2"
        },
        "42": {
            "row": "6",
            "column": "0",
            "type": "2"
        },
        "43": {
            "row": "6",
            "column": "1",
            "type": "2"
        },
        "44": {
            "row": "6",
            "column": "2",
            "type": "2"
        },
        "45": {
            "row": "6",
            "column": "3",
            "type": "2"
        },
        "46": {
            "row": "6",
            "column": "4",
            "type": "2"
        },
        "47": {
            "row": "6",
            "column": "5",
            "type": "2"
        },
        "48": {
            "row": "5",
            "column": "6",
            "type": "2"
        },
        "49": {
            "row": "4",
            "column": "6",
            "type": "2"
        },
        "50": {
            "row": "3",
            "column": "6",
            "type": "2"
        },
        "51": {
            "row": "2",
            "column": "6",
            "type": "2"
        },
        "52": {
            "row": "1",
            "column": "6",
            "type": "2"
        },
        "53": {
            "row": "0",
            "column": "6",
            "type": "2"
        },
        "54": {
            "row": "0",
            "column": "7",
            "type": "2"
        },
        "55": {
            "row": "1",
            "column": "7",
            "type": "3"
        },
        "56": {
            "row": "2",
            "column": "7",
            "type": "3"
        },
        "57": {
            "row": "3",
            "column": "7",
            "type": "3"
        },
        "58": {
            "row": "4",
            "column": "7",
            "type": "3"
        },
        "59": {
            "row": "5",
            "column": "7",
            "type": "3"
        },
        "60": {
            "row": "6",
            "column": "7",
            "type": "3"
        }
    }


def _get_player_three_moves():
    return {
        "0": {
            "row": "11",
            "column": "12",
            "type": "1"
        },
        "1": {
            "row": "12",
            "column": "12",
            "type": "1"
        },
        "2": {
            "row": "12",
            "column": "11",
            "type": "1"
        },
        "3": {
            "row": "11",
            "column": "11",
            "type": "1"
        },
        "4": {
            "row": "8",
            "column": "13",
            "type": "2"
        },
        "5": {
            "row": "8",
            "column": "12",
            "type": "2"
        },
        "6": {
            "row": "8",
            "column": "11",
            "type": "2"
        },
        "7": {
            "row": "8",
            "column": "10",
            "type": "2"
        },
        "8": {
            "row": "8",
            "column": "9",
            "type": "2"
        },
        "9": {
            "row": "9",
            "column": "8",
            "type": "2"
        },
        "10": {
            "row": "10",
            "column": "8",
            "type": "2"
        },
        "11": {
            "row": "11",
            "column": "8",
            "type": "2"
        },
        "12": {
            "row": "12",
            "column": "8",
            "type": "2"
        },
        "13": {
            "row": "13",
            "column": "8",
            "type": "2"
        },
        "14": {
            "row": "14",
            "column": "8",
            "type": "2"
        },
        "15": {
            "row": "14",
            "column": "7",
            "type": "2"
        },
        "16": {
            "row": "14",
            "column": "6",
            "type": "2"
        },
        "17": {
            "row": "13",
            "column": "6",
            "type": "2"
        },
        "18": {
            "row": "12",
            "column": "6",
            "type": "2"
        },
        "19": {
            "row": "11",
            "column": "6",
            "type": "2"
        },
        "20": {
            "row": "10",
            "column": "6",
            "type": "2"
        },
        "21": {
            "row": "9",
            "column": "6",
            "type": "2"
        },
        "22": {
            "row": "8",
            "column": "5",
            "type": "2"
        },
        "23": {
            "row": "8",
            "column": "4",
            "type": "2"
        },
        "24": {
            "row": "8",
            "column": "3",
            "type": "2"
        },
        "25": {
            "row": "8",
            "column": "2",
            "type": "2"
        },
        "26": {
            "row": "8",
            "column": "1",
            "type": "2"
        },
        "27": {
            "row": "8",
            "column": "0",
            "type": "2"
        },
        "28": {
            "row": "7",
            "column": "0",
            "type": "2"
        },
        "29": {
            "row": "6",
            "column": "0",
            "type": "2"
        },
        "30": {
            "row": "6",
            "column": "1",
            "type": "2"
        },
        "31": {
            "row": "6",
            "column": "2",
            "type": "2"
        },
        "32": {
            "row": "6",
            "column": "3",
            "type": "2"
        },
        "33": {
            "row": "6",
            "column": "4",
            "type": "2"
        },
        "34": {
            "row": "6",
            "column": "5",
            "type": "2"
        },
        "35": {
            "row": "5",
            "column": "6",
            "type": "2"
        },
        "36": {
            "row": "4",
            "column": "6",
            "type": "2"
        },
        "37": {
            "row": "3",
            "column": "6",
            "type": "2"
        },
        "38": {
            "row": "2",
            "column": "6",
            "type": "2"
        },
        "39": {
            "row": "1",
            "column": "6",
            "type": "2"
        },
        "40": {
            "row": "0",
            "column": "6",
            "type": "2"
        },
        "41": {
            "row": "0",
            "column": "7",
            "type": "2"
        },
        "42": {
            "row": "0",
            "column": "8",
            "type": "2"
        },
        "43": {
            "row": "1",
            "column": "8",
            "type": "2"
        },
        "44": {
            "row": "2",
            "column": "8",
            "type": "2"
        },
        "45": {
            "row": "3",
            "column": "8",
            "type": "2"
        },
        "46": {
            "row": "4",
            "column": "8",
            "type": "2"
        },
        "47": {
            "row": "5",
            "column": "8",
            "type": "2"
        },
        "48": {
            "row": "6",
            "column": "9",
            "type": "2"
        },
        "49": {
            "row": "6",
            "column": "10",
            "type": "2"
        },
        "50": {
            "row": "6",
            "column": "11",
            "type": "2"
        },
        "51": {
            "row": "6",
            "column": "12",
            "type": "2"
        },
        "52": {
            "row": "6",
            "column": "13",
            "type": "2"
        },
        "53": {
            "row": "6",
            "column": "14",
            "type": "2"
        },
        "54": {
            "row": "7",
            "column": "14",
            "type": "2"
        },
        "55": {
            "row": "7",
            "column": "13",
            "type": "3"
        },
        "56": {
            "row": "7",
            "column": "12",
            "type": "3"
        },
        "57": {
            "row": "7",
            "column": "11",
            "type": "3"
        },
        "58": {
            "row": "7",
            "column": "10",
            "type": "3"
        },
        "59": {
            "row": "7",
            "column": "9",
            "type": "3"
        },
        "60": {
            "row": "7",
            "column": "8",
            "type": "3"
        }
    }


def _get_player_four_moves():
    return {
        "0": {
            "row": "11",
            "column": "2",
            "type": "1"
        },
        "1": {
            "row": "12",
            "column": "2",
            "type": "1"
        },
        "2": {
            "row": "11",
            "column": "3",
            "type": "1"
        },
        "3": {
            "row": "12",
            "column": "3",
            "type": "1"
        },
        "4": {
            "row": "13",
            "column": "6",
            "type": "2"
        },
        "5": {
            "row": "12",
            "column": "6",
            "type": "2"
        },
        "6": {
            "row": "11",
            "column": "6",
            "type": "2"
        },
        "7": {
            "row": "10",
            "column": "6",
            "type": "2"
        },
        "8": {
            "row": "9",
            "column": "6",
            "type": "2"
        },
        "9": {
            "row": "8",
            "column": "5",
            "type": "2"
        },
        "10": {
            "row": "8",
            "column": "4",
            "type": "2"
        },
        "11": {
            "row": "8",
            "column": "3",
            "type": "2"
        },
        "12": {
            "row": "8",
            "column": "2",
            "type": "2"
        },
        "13": {
            "row": "8",
            "column": "1",
            "type": "2"
        },
        "14": {
            "row": "8",
            "column": "0",
            "type": "2"
        },
        "15": {
            "row": "7",
            "column": "0",
            "type": "2"
        },
        "16": {
            "row": "6",
            "column": "0",
            "type": "2"
        },
        "17": {
            "row": "6",
            "column": "1",
            "type": "2"
        },
        "18": {
            "row": "6",
            "column": "2",
            "type": "2"
        },
        "19": {
            "row": "6",
            "column": "3",
            "type": "2"
        },
        "20": {
            "row": "6",
            "column": "4",
            "type": "2"
        },
        "21": {
            "row": "6",
            "column": "5",
            "type": "2"
        },
        "22": {
            "row": "5",
            "column": "6",
            "type": "2"
        },
        "23": {
            "row": "4",
            "column": "6",
            "type": "2"
        },
        "24": {
            "row": "3",
            "column": "6",
            "type": "2"
        },
        "25": {
            "row": "2",
            "column": "6",
            "type": "2"
        },
        "26": {
            "row": "1",
            "column": "6",
            "type": "2"
        },
        "27": {
            "row": "0",
            "column": "6",
            "type": "2"
        },
        "28": {
            "row": "0",
            "column": "7",
            "type": "2"
        },
        "29": {
            "row": "0",
            "column": "8",
            "type": "2"
        },
        "30": {
            "row": "1",
            "column": "8",
            "type": "2"
        },
        "31": {
            "row": "2",
            "column": "8",
            "type": "2"
        },
        "32": {
            "row": "3",
            "column": "8",
            "type": "2"
        },
        "33": {
            "row": "4",
            "column": "8",
            "type": "2"
        },
        "34": {
            "row": "5",
            "column": "8",
            "type": "2"
        },
        "35": {
            "row": "6",
            "column": "9",
            "type": "2"
        },
        "36": {
            "row": "6",
            "column": "10",
            "type": "2"
        },
        "37": {
            "row": "6",
            "column": "11",
            "type": "2"
        },
        "38": {
            "row": "6",
            "column": "12",
            "type": "2"
        },
        "39": {
            "row": "6",
            "column": "13",
            "type": "2"
        },
        "40": {
            "row": "6",
            "column": "14",
            "type": "2"
        },
        "41": {
            "row": "7",
            "column": "14",
            "type": "2"
        },
        "42": {
            "row": "8",
            "column": "14",
            "type": "2"
        },
        "43": {
            "row": "8",
            "column": "13",
            "type": "2"
        },
        "44": {
            "row": "8",
            "column": "12",
            "type": "2"
        },
        "45": {
            "row": "8",
            "column": "11",
            "type": "2"
        },
        "46": {
            "row": "8",
            "column": "10",
            "type": "2"
        },
        "47": {
            "row": "8",
            "column": "9",
            "type": "2"
        },
        "48": {
            "row": "9",
            "column": "8",
            "type": "2"
        },
        "49": {
            "row": "10",
            "column": "8",
            "type": "2"
        },
        "50": {
            "row": "11",
            "column": "8",
            "type": "2"
        },
        "51": {
            "row": "12",
            "column": "8",
            "type": "2"
        },
        "52": {
            "row": "13",
            "column": "8",
            "type": "2"
        },
        "53": {
            "row": "14",
            "column": "8",
            "type": "2"
        },
        "54": {
            "row": "14",
            "column": "7",
            "type": "2"
        },
        "55": {
            "row": "13",
            "column": "7",
            "type": "3"
        },
        "56": {
            "row": "12",
            "column": "7",
            "type": "3"
        },
        "57": {
            "row": "11",
            "column": "7",
            "type": "3"
        },
        "58": {
            "row": "10",
            "column": "7",
            "type": "3"
        },
        "59": {
            "row": "9",
            "column": "7",
            "type": "3"
        },
        "60": {
            "row": "8",
            "column": "7",
            "type": "3"
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
        [' ', ' ', ' ', ' ', ' ', ' ', 'b', 'b', 'b', ' ', ' ', ' ', ' ', ' ',
         ' '],
        [' ', '1', '-', '-', '2', ' ', 'b', 'b', 'b', ' ', '1', '-', '-', '2',
         ' '],
        [' ', '|', 'q', 'q', '|', ' ', 'b', 'b', 'b', ' ', '|', 'w', 'w', '|',
         ' '],
        [' ', '|', 'q', 'q', '|', ' ', 'b', 'b', 'b', ' ', '|', 'w', 'w', '|',
         ' '],
        [' ', '4', '-', '-', '3', ' ', 'b', 'b', 'b', ' ', '4', '-', '-', '3',
         ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', 'b', 'b', 'b', ' ', ' ', ' ', ' ', ' ',
         ' '],
        ['b', 'b', 'b', 'b', 'b', 'b', ' ', ' ', ' ', 'b', 'b', 'b', 'b', 'b',
         'b'],
        ['b', 'b', 'b', 'b', 'b', 'b', ' ', ' ', ' ', 'b', 'b', 'b', 'b', 'b',
         'b'],
        ['b', 'b', 'b', 'b', 'b', 'b', ' ', ' ', ' ', 'b', 'b', 'b', 'b', 'b',
         'b'],
        [' ', ' ', ' ', ' ', ' ', ' ', 'b', 'b', 'b', ' ', ' ', ' ', ' ', ' ',
         ' '],
        [' ', '1', '-', '-', '2', ' ', 'b', 'b', 'b', ' ', '1', '-', '-', '2',
         ' '],
        [' ', '|', 'e', 'e', '|', ' ', 'b', 'b', 'b', ' ', '|', 'r', 'r', '|',
         ' '],
        [' ', '|', 'e', 'e', '|', ' ', 'b', 'b', 'b', ' ', '|', 'r', 'r', '|',
         ' '],
        [' ', '4', '-', '-', '3', ' ', 'b', 'b', 'b', ' ', '4', '-', '-', '3',
         ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', 'b', 'b', 'b', ' ', ' ', ' ', ' ', ' ',
         ' '],
    ]
