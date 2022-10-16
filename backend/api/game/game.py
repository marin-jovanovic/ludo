import sys
from random import SystemRandom
from collections import defaultdict

def get_dice_result():
    crypto_generator_object = SystemRandom()
    return crypto_generator_object.randrange(6) + 1

def get_player_one_moves():
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

        # highest: highest goes first and then clockwise or anticlockwise
        # order: 1st, 2nd, 3rd, 4th highest roll
        'choice: highest; order': True,

        # if highest then in which direction
        'choice: clockwise; anticlockwise': True

    }

class Tile:

    def __init__(self, row, column):
        self.row = row
        self.column = column

        # self.visitors = set()

    # def add_visitor(self, visitor):
    #     if visitor in self.visitors:
    #         print("visitor already in this")
    #         sys.exit(-1)
    #
    #     self.visitors.add(visitor)

    def __str__(self):
        return f"row: {self.row}, column: {self.column}"

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Tile):
            return self.row == other.row and self.column == other.column
        return False

        # def __eq__(self, other):
        #     if isinstance(other, self.__class__):
        #         return self.__dict__ == other.__dict__
        #     else:
        #         return False
        # return NotImplemented

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(tuple(sorted(self.__dict__.items())))


class TileVisitor:

    def __init__(self, player, players_tile_translation_id):
        self.player = player
        self.players_tile_translation_id = players_tile_translation_id

    def __str__(self):
        return f"player: {self.player}, tile: {self.players_tile_translation_id}"

class Token:

    def __init__(
        self,
        owner,
        current_tile,
        destination_tile
    ):
        self.owner = owner

        self.current_tile = current_tile

        self.destination_tile = destination_tile

    def can_move(self):
        return self.current_tile != self.destination_tile

    def move(self, step):

        print('move token')


def determine_order(number_of_players, choice_highest_or_order, choice_clockwise_or_anticlockwise):

    # def get_max()

    # order =
    roll_history = []

    needs_to_roll = {i: True for i in range(number_of_players)}

    while True:
        print()
        if sum([v for _, v in needs_to_roll.items()]) == 1:
            print('one player left, he is last')
            break

        # for i in [v for k,v in needs_to_roll.items()]:
        #     print()

        r = {}
        for player, f_needs_to_roll in needs_to_roll.items():
            if not f_needs_to_roll:
                continue

            r[player] = get_dice_result()

        [print(i) for i in r.items()]
        # break

        # r = [get_dice_result() for _ in [v for k,v in needs_to_roll.items()]]

        for i, v in enumerate(r.items()):
            roll_history.append({'player': i, 'result': v[1]})

        print('roll history')
        [print(i) for i in roll_history]

        while True:
            m = max([roll for _, roll in r.items()])
            # print('max', m)
            c_m = 0
            m_player = -1
            for player, result in r.items():
                if m == result:
                    c_m += 1
                    m_player = player

            # c_m = sum([1 for i in r if i == m])
            # print('count max', c_m)

            if c_m == 1:
                winner = m_player
                print('first goes', winner)
                roll_history.append(['goes', winner])
                needs_to_roll[winner] = False
                # r.remove(m)

                print(f'{r=}')
                print(f'{needs_to_roll=}')
                # print(r.index(m))

            else:
                print('tie, must roll again')
                break

            break

        t = get_dice_result()
        print(t)
        break

    [print(i) for i in roll_history]
    return [1, 2, 3, 4]
    pass

def main():
    # p = {
    #     1: get_player_one_moves(),
    #     2: get_player_two_moves(),
    #     3: get_player_one_moves()
    # }
    #
    # m_tile_to_move = generate_tile_mapping(p)
    #
    # # print(len(m_tile_to_move))
    # for tile, tile_id in m_tile_to_move.items():
    #     print(tile, '=>', [str(i) for i in tile_id])

    game_conf = get_config()

    order = determine_order(game_conf['number of players'],
                            game_conf['choice: highest; order'],
                            game_conf['choice: clockwise; anticlockwise']
                            )

    print(f"{order=}")


    #

    # roled = 6
    #
    # player_1_token_1 = Token(owner=1, current_tile=Tile(0, 0), destination_tile=None)

def generate_tile_mapping(p):
    m_tile_to_move = defaultdict(set)
    for player_id, moves in p.items():

        for tile_id, coordinates in moves.items():

            tile = Tile(**coordinates)
            # if tile in m_tile_to_move:
            #     print('already in coordinates')
            #     sys.exit(-1)
            #     # break
            #
            # else:
            tile_visitor = TileVisitor(player_id, tile_id)

            if tile_visitor in m_tile_to_move[tile]:
                print('add error')
                sys.exit(-1)

            m_tile_to_move[tile].add(tile_visitor)
    return m_tile_to_move


if __name__ == '__main__':
    main()