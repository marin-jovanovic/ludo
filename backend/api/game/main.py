def main():
    """
    each player has tokens
    each player does not have to have same number of tokens

    each token can have only one starting point
    when token is eaten it goes to starting point

    token can be in one of three pools
    token can not be in multiple pools at the same time

    pools are "init", "main", "safe", "end"

    tile id
        main pool
            relative
            absolute

        other
            relative

    """

    # turn -> user id
    order = {
        0: 2,
        1: 3,
        2: 0,
        3: 1,
    }

    moves = {
        "0": {
            -1: {
                "type": "init"
            },
            0: {
                "type": ""
            }

        }
    }

    for turn, user_id in order.items():
        print(f"{turn=} {user_id=}")


if __name__ == '__main__':
    main()